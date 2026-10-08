#!/usr/bin/env python3
"""Migração única e idempotente: corrige o estado deste estudo para o contrato ai-tutor v2.

Aplica o plano de docs/plano-correcao-estado.md (itens 1 a 6), com as opções recomendadas:

1. sources.json: renomeia author, published_or_updated, type e why_authoritative e
   acrescenta lesson_ids. Quando a data publicada é só o ano, ele vai para
   publication_year e publication_date fica null.
2. state.diagnostics[0]: reescreve as observações e o summary no formato do
   diagnostic-contract.
3. Diagnóstico não é evidência: tira as evidências kind="diagnostic" de evidences,
   dos tópicos e da sessão do diagnóstico e grava topics[].diagnostic. Os tópicos
   que só tinham diagnóstico voltam a mastery 0.
4. reference.type "conversation" vira "session", e o id antigo vai para location.
5. O ponto fraco passa a usar supporting_evidence_ids=[] e status "active", com
   uma nota que cita as observações de origem.
6. project_m01_contexto ganha name.

Primeiro, a migração roda numa cópia temporária e passa pelo validate_study. Só
depois grava os arquivos canônicos com atomic_update_json e expected_revision.

Uso:
    python 2026-10-07-correcao-estado.py --study-root <dir> --skill-root <dir> [--apply]
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

DIAGNOSTIC_ID = "diagnostic_entrada_001"
M01_LESSON_ID = "lesson_m01_modelos_tokens_contexto"
M01_TOPIC_ID = "topic_modelos_tokens_contexto"
M01_SOURCE_IDS = {"source_anthropic_context_eng", "source_huyen_ai_eng", "source_from_scratch"}
PROJECT_NAME = "M01 · Modelos, tokens, contexto e reasoning"
WEAK_POINT_ID = "weak_01ebbe5b-9c4a-40fa-89a1-4f0b4f7ee885"
SOURCE_RENAMES = {
    "author": "author_or_institution",
    "published_or_updated": "publication_date",
    "type": "source_type",
    "why_authoritative": "authority_reason",
}
# Plano, item 2: 40 vira likely_known e 20 vira partial; resultado incorrect ou
# lacuna declarada vira weak.
ESTIMATE_BY_MASTERY = {40: "likely_known", 20: "partial", 0: "weak"}
# Direção que o contrato associa a cada sinal: sucesso aprofunda, lacuna
# investiga o pré-requisito, sinal parcial testa em outro contexto.
DIRECTION_BY_ESTIMATE = {"likely_known": "probe_up", "partial": "probe_across", "weak": "probe_down"}
# A nota do diagnóstico aponta a arquitetura (camadas da aplicação) como base das demais.
PREREQUISITE_GAP_TOPICS = {"topic_arquitetura_aplicacao"}
SYNTHESIS_PREFIX = "[Síntese do tutor; a resposta literal não foi registrada] "


class MigrationError(RuntimeError):
    """O estudo não pode ser migrado com segurança."""


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def already_migrated(state: dict, sources: dict) -> bool:
    no_diagnostic_evidence = all(e.get("kind") != "diagnostic" for e in state["evidences"])
    sources_ok = all("author_or_institution" in s for s in sources["sources"])
    return no_diagnostic_evidence and sources_ok


def migrate_sources(sources: dict) -> dict:
    for source in sources["sources"]:
        for old, new in SOURCE_RENAMES.items():
            if old in source and new not in source:
                source[new] = source.pop(old)
        date_value = source.get("publication_date")
        if isinstance(date_value, str) and len(date_value) == 4 and date_value.isdigit():
            # Só o ano é conhecido; o contrato exige data ISO, e não se inventa o dia.
            source["publication_year"] = date_value
            source["publication_date"] = None
        if "lesson_ids" not in source:
            source["lesson_ids"] = [M01_LESSON_ID] if source["source_id"] in M01_SOURCE_IDS else []
    return sources


def question_number(evidence: dict) -> str:
    return evidence["reference"]["id"].rsplit("/", 1)[-1]


def build_observations(state: dict, diagnostic: dict, topic_mastery: dict) -> list[dict]:
    """Monta as observações do contrato a partir das evidências diagnósticas e das notas."""

    old_observations = {o["topic_id"]: o for o in diagnostic["observations"]}
    diagnostic_evidences = [e for e in state["evidences"] if e.get("kind") == "diagnostic"]

    observations = []
    for evidence in diagnostic_evidences:
        topic_id = evidence["topic_id"]
        note = old_observations.get(topic_id, {}).get("note")
        if evidence["result"] == "incorrect":
            estimate = "weak"
        else:
            estimate = ESTIMATE_BY_MASTERY[topic_mastery[topic_id]]
        response_basis = note or evidence["error"]
        reason_parts = [part for part in (evidence["error"], note) if part]
        observations.append({
            "observation_id": f"diagnostic_observation_entrada_001_{question_number(evidence)}",
            "topic_id": topic_id,
            "prompt": evidence["context"].removeprefix("diagnóstico: "),
            "response": SYNTHESIS_PREFIX + response_basis,
            "estimate": estimate,
            "confidence": "low",
            "direction": DIRECTION_BY_ESTIMATE[estimate],
            "prerequisite_gap": topic_id in PREREQUISITE_GAP_TOPICS,
            "reason": f"Resultado {evidence['result']}. " + " | ".join(reason_parts),
            "recorded_at": evidence["recorded_at"],
            "legacy_evidence_id": evidence["evidence_id"],
        })

    # Q4 (memória) nunca virou evidência; a nota antiga é o único registro.
    for topic_id, old in old_observations.items():
        if old.get("evidence_id") is None and old.get("note"):
            observations.append({
                "observation_id": "diagnostic_observation_entrada_001_q4",
                "topic_id": topic_id,
                "prompt": "memória entre sessões em chatbot de loja",
                "response": SYNTHESIS_PREFIX + "Declarou não ter ideia.",
                "estimate": "weak",
                "confidence": "low",
                "direction": "probe_down",
                "prerequisite_gap": topic_id in PREREQUISITE_GAP_TOPICS,
                "reason": old["note"],
                "recorded_at": old["recorded_at"],
            })

    observations.sort(key=lambda o: int(o["observation_id"].rsplit("_q", 1)[-1]))
    return observations


def migrate_state(state: dict) -> dict:
    diagnostic = next(d for d in state["diagnostics"] if d["diagnostic_id"] == DIAGNOSTIC_ID)
    topic_mastery = {t["topic_id"]: t["mastery"] for t in state["topics"]}
    diagnostic_evidence_ids = {e["evidence_id"] for e in state["evidences"] if e.get("kind") == "diagnostic"}

    # Item 2: observações e summary no formato do contrato.
    observations = build_observations(state, diagnostic, topic_mastery)
    diagnostic["summary_notes"] = diagnostic["summary"]  # frases antigas, preservadas para leitura
    diagnostic["observations"] = observations
    diagnostic["summary"] = [
        {
            "topic_id": o["topic_id"],
            "estimate": o["estimate"],
            "confidence": o["confidence"],
            "observation_ids": [o["observation_id"]],
        }
        for o in observations
    ]
    diagnostic["entry_topic_id"] = M01_TOPIC_ID

    # Item 3: as observações saem de evidences e o domínio é recalculado.
    estimate_by_topic = {o["topic_id"]: o for o in observations}
    state["evidences"] = [e for e in state["evidences"] if e["evidence_id"] not in diagnostic_evidence_ids]
    for topic in state["topics"]:
        topic["evidence_ids"] = [i for i in topic["evidence_ids"] if i not in diagnostic_evidence_ids]
        observation = estimate_by_topic.get(topic["topic_id"])
        if observation:
            topic["diagnostic"] = {
                "estimate": observation["estimate"],
                "confidence": observation["confidence"],
                "diagnostic_id": DIAGNOSTIC_ID,
            }
        if not topic["evidence_ids"]:
            topic["mastery"] = 0
            topic["status"] = "not_started"
            topic["last_practice"] = None
    for session in state["sessions"]:
        removed = [i for i in session.get("evidence_ids", []) if i in diagnostic_evidence_ids]
        if removed:
            session["evidence_ids"] = [i for i in session["evidence_ids"] if i not in diagnostic_evidence_ids]
            session["diagnostic_id"] = DIAGNOSTIC_ID
            session["migration_note"] = (
                "2026-10-07: as respostas deste diagnóstico deixaram de ser evidências "
                f"e estão em diagnostics[{DIAGNOSTIC_ID}].observations."
            )
    for observation in observations:
        observation.pop("legacy_evidence_id", None)

    # Item 4: referência para a sessão real, preservando o rótulo antigo.
    for evidence in state["evidences"]:
        reference = evidence["reference"]
        if reference.get("type") == "conversation":
            evidence["reference"] = {
                "type": "session",
                "id": evidence["session_id"],
                "location": reference["id"],
            }

    # Item 5: o ponto fraco continua ativo, sem evidência de aula por enquanto.
    for weak_point in state["weak_points"]:
        if weak_point["weak_point_id"] != WEAK_POINT_ID:
            continue
        legacy = weak_point.pop("evidence_ids", None)
        weak_point.setdefault("supporting_evidence_ids", [])
        if weak_point.get("status") == "open":
            weak_point["status"] = "active"
        if legacy is not None:
            origin = sorted(
                o["observation_id"]
                for o in observations
                if o["topic_id"] in {"topic_prompts_interface", "topic_tools_function_calling", "topic_seguranca_harness"}
            )
            weak_point["note"] = (
                "Originado no diagnóstico de entrada, observado três vezes: "
                + ", ".join(origin)
                + ". Observações diagnósticas não são evidência; aguarda evidência de aula."
            )

    # Item 6.
    for project in state["projects"]:
        if project["project_id"] == "project_m01_contexto":
            project.setdefault("name", PROJECT_NAME)

    state["updated_at"] = now_iso()
    return state


def validate(skill_root: Path, study_root: Path) -> tuple[bool, str]:
    result = subprocess.run(
        [sys.executable, "-m", "scripts.validate_study", str(study_root)],
        cwd=skill_root, capture_output=True, text=True, encoding="utf-8",
    )
    output = result.stdout + result.stderr
    return "STUDY VALIDATION: PASS" in output, output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--study-root", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="grava os arquivos canônicos")
    args = parser.parse_args()
    args.study_root, args.skill_root = args.study_root.resolve(), args.skill_root.resolve()

    tutor_dir = args.study_root / ".ai-tutor"
    state_path, sources_path = tutor_dir / "state.json", tutor_dir / "sources.json"
    state, sources = read_json(state_path), read_json(sources_path)

    if already_migrated(state, sources):
        print("Nada a fazer: o estado já está migrado.")
        return 0

    new_state = migrate_state(copy.deepcopy(state))
    new_sources = migrate_sources(copy.deepcopy(sources))

    with tempfile.TemporaryDirectory() as tmp:
        staging = Path(tmp) / "study"
        shutil.copytree(args.study_root, staging, ignore=shutil.ignore_patterns(".git"))
        (staging / ".ai-tutor/state.json").write_text(json.dumps(new_state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (staging / ".ai-tutor/sources.json").write_text(json.dumps(new_sources, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        ok, output = validate(args.skill_root, staging)
    print(output.strip())
    if not ok:
        raise MigrationError("a cópia migrada não passou no validate_study; nada foi gravado")

    if not args.apply:
        print("Simulação concluída. Rode com --apply para gravar.")
        return 0

    sys.path.insert(0, str(args.skill_root))
    from scripts.state_io import atomic_update_json

    atomic_update_json(state_path, lambda _: new_state, expected_revision=state["revision"])
    atomic_update_json(sources_path, lambda _: new_sources, expected_revision=sources["revision"])
    ok, output = validate(args.skill_root, args.study_root)
    print(output.strip())
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
