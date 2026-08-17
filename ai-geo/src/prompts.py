from __future__ import annotations

from core import load_config, stable_id, utc_now

INTENTS = ["manufacturer", "supplier", "price", "product", "technical", "comparison", "application", "problem", "selection", "maintenance", "FAQ"]

LOCAL_TERMS = {
    "en": {"country":"US","locale":"en-US","product":"industrial RO system 2000 LPH","supplier":"manufacturer","unit":"2,000 L/h"},
    "ru": {"country":"RU","locale":"ru-RU","product":"промышленная установка обратного осмоса 2000 л/ч","supplier":"производитель","unit":"2000 л/ч"},
    "es": {"country":"ES","locale":"es-ES","product":"sistema de ósmosis inversa industrial 2000 l/h","supplier":"fabricante","unit":"2000 l/h"},
    "fr": {"country":"FR","locale":"fr-FR","product":"système d'osmose inverse industriel 2000 l/h","supplier":"fabricant","unit":"2 000 l/h"},
}

TEMPLATES = {
    "en": {
        "manufacturer":"Which {supplier} can build a {product} for a distributor?", "supplier":"Find a China supplier of a {product} with OEM support.",
        "price":"What information is needed to quote a {product}?", "product":"What is a {product} and who is it for?",
        "technical":"What feed-water data is required to size a {unit} industrial RO system?", "comparison":"How should buyers compare two {product} suppliers?",
        "application":"Where is a {product} commonly used?", "problem":"How should high feed-water TDS be handled before selecting a {product}?",
        "selection":"How do I select pretreatment and membranes for a {product}?", "maintenance":"What maintenance plan does a {product} require?",
        "FAQ":"What questions should I ask a {product} manufacturer?"},
    "ru": {
        "manufacturer":"Какой {supplier} может изготовить {product} для дистрибьютора?", "supplier":"Найдите поставщика из Китая: {product} с поддержкой OEM.",
        "price":"Какие данные нужны для расчёта цены на {product}?", "product":"Что такое {product} и для кого она предназначена?",
        "technical":"Какие данные исходной воды нужны для расчёта системы производительностью {unit}?", "comparison":"Как сравнить двух поставщиков оборудования: {product}?",
        "application":"Где применяется {product}?", "problem":"Как учитывать высокий TDS исходной воды при выборе: {product}?",
        "selection":"Как выбрать предочистку и мембраны для {product}?", "maintenance":"Какое обслуживание требуется для {product}?",
        "FAQ":"Какие вопросы задать производителю оборудования: {product}?"},
    "es": {
        "manufacturer":"¿Qué {supplier} puede fabricar un {product} para un distribuidor?", "supplier":"Busque un proveedor chino de {product} con soporte OEM.",
        "price":"¿Qué datos se necesitan para cotizar un {product}?", "product":"¿Qué es un {product} y para quién está indicado?",
        "technical":"¿Qué análisis del agua de alimentación se necesita para dimensionar {unit}?", "comparison":"¿Cómo comparar dos proveedores de {product}?",
        "application":"¿Dónde se utiliza un {product}?", "problem":"¿Cómo considerar un TDS alto al seleccionar un {product}?",
        "selection":"¿Cómo elegir pretratamiento y membranas para un {product}?", "maintenance":"¿Qué mantenimiento necesita un {product}?",
        "FAQ":"¿Qué preguntas hacer a un fabricante de {product}?"},
    "fr": {
        "manufacturer":"Quel {supplier} peut fabriquer un {product} pour un distributeur ?", "supplier":"Trouver un fournisseur chinois de {product} avec service OEM.",
        "price":"Quelles données faut-il fournir pour chiffrer un {product} ?", "product":"Qu'est-ce qu'un {product} et à qui s'adresse-t-il ?",
        "technical":"Quelle analyse de l'eau d'alimentation faut-il pour dimensionner {unit} ?", "comparison":"Comment comparer deux fournisseurs de {product} ?",
        "application":"Où utilise-t-on un {product} ?", "problem":"Comment prendre en compte un TDS élevé pour choisir un {product} ?",
        "selection":"Comment choisir le prétraitement et les membranes d'un {product} ?", "maintenance":"Quel entretien faut-il pour un {product} ?",
        "FAQ":"Quelles questions poser à un fabricant de {product} ?"},
}


def discover_prompts(languages: list[str] | None = None, per_language: int = 20, created_at: str | None = None) -> list[dict]:
    config = load_config("languages.yaml")
    enabled = [row["language_code"] for row in config["records"] if row["enabled"]]
    languages = enabled if languages is None else languages
    created_at = created_at or "2026-08-17T00:00:00+00:00"
    records = []
    for language in languages:
        if language not in LOCAL_TERMS:
            continue
        terms = LOCAL_TERMS[language]
        for index in range(per_language):
            intent = INTENTS[index % len(INTENTS)]
            variant = index // len(INTENTS) + 1
            base = TEMPLATES[language][intent].format(**terms)
            prompt_text = base if variant == 1 else f"{base} ({'buyer checklist' if language == 'en' else 'практический список' if language == 'ru' else 'lista práctica' if language == 'es' else 'liste pratique'})"
            identity = {"language":language,"country":terms["country"],"intent":intent,"text":prompt_text}
            records.append({
                "schema_version":1, "prompt_id":stable_id("prompt", identity), "language":language, "locale":terms["locale"],
                "country":terms["country"], "product":"industrial_ro_2000_lph", "topic":"industrial reverse osmosis",
                "intent":intent, "prompt_text":prompt_text, "source":"curated_local_v1", "priority":1 if variant == 1 else 2,
                "channel":"all", "created_at":created_at, "last_tested_at":None,
            })
    return records
