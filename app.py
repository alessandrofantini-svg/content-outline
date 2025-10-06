"""Streamlit SEO prompt ideation tool leveraging DataForSEO and OpenAI APIs."""
from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import Iterable, List, Optional

import requests
import streamlit as st
from bs4 import BeautifulSoup
from openai import OpenAI

DATAFORSEO_ENDPOINT = "https://api.dataforseo.com/v3/serp/google/organic/live/regular"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


@dataclass
class SerpResult:
    position: int
    title: str
    url: str
    snippet: str


def fetch_serp_results(
    keyword: str,
    location_name: str,
    language_name: str,
    limit: int,
    login: str,
    password: str,
    device: str = "desktop",
) -> List[SerpResult]:
    """Fetch SERP results from DataForSEO."""
    payload = {
        "keyword": keyword,
        "location_name": location_name,
        "language_name": language_name,
        "device": device,
        "depth": limit,
    }
    response = requests.post(
        DATAFORSEO_ENDPOINT,
        auth=(login, password),
        json={"data": [payload]},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    tasks = data.get("tasks", [])
    if not tasks:
        raise ValueError("La risposta dell'API DataForSEO non contiene task.")

    results: List[SerpResult] = []
    for task in tasks:
        for result in task.get("result", []):
            items = result.get("items", [])
            for item in items:
                if item.get("type") != "organic" or "url" not in item:
                    continue
                serp_result = SerpResult(
                    position=item.get("rank_group", 0),
                    title=item.get("title", ""),
                    url=item["url"],
                    snippet=item.get("snippet", ""),
                )
                results.append(serp_result)
    return results[:limit]


def extract_text_from_html(html: str) -> str:
    """Extract readable text from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    text = "\n".join(paragraphs)
    return textwrap.shorten(text, width=2000, placeholder="…")


def fetch_competitor_content(url: str, timeout: int = 20) -> Optional[str]:
    """Download and extract competitor page content."""
    headers = {"User-Agent": DEFAULT_USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException:
        return None
    return extract_text_from_html(response.text)


def build_competitor_brief(results: Iterable[SerpResult], max_competitors: int = 5) -> str:
    """Create a compact summary of competitor content."""
    briefs: List[str] = []
    for result in list(results)[:max_competitors]:
        content = fetch_competitor_content(result.url)
        if not content:
            briefs.append(
                f"- **{result.title}** ({result.url})\n  - Contenuto non disponibile, usa il titolo e lo snippet per l'analisi."
            )
            continue
        briefs.append(
            f"- **{result.title}** ({result.url})\n  - Estratto: {textwrap.shorten(content, width=350, placeholder='…')}"
        )
    return "\n".join(briefs)


def generate_seo_prompts(
    client: OpenAI,
    query: str,
    location: str,
    language: str,
    serp_overview: List[SerpResult],
    competitor_brief: str,
    tone: str,
    audience: str,
    additional_notes: str,
) -> str:
    """Generate SEO prompts leveraging OpenAI."""
    serp_table = "\n".join(
        f"{item.position}. {item.title} — {item.url}\n   Snippet: {item.snippet}" for item in serp_overview
    )

    user_prompt = f"""
    Sei un consulente SEO senior incaricato di definire un contenuto che si posizioni
    per la query: "{query}".

    Dati disponibili:
    - Località target: {location}
    - Lingua target: {language}
    - Pubblico di riferimento: {audience or 'non specificato'}
    - Tono di voce richiesto: {tone or 'neutro'}
    - Note aggiuntive: {additional_notes or 'nessuna'}

    Panoramica SERP attuale:
    {serp_table}

    Insight dai competitor:
    {competitor_brief or 'Non sono disponibili contenuti da mostrare.'}

    Produci una proposta completa per il contenuto che includa:
    1. Obiettivo principale del contenuto e KPI.
    2. Analisi dell'intento di ricerca con micro-intenti correlati.
    3. Struttura dettagliata (H1, H2, H3) con descrizione per ogni sezione.
    4. Suggerimenti di paragrafi chiave e punti da trattare.
    5. Lista di parole chiave e varianti a coda lunga, con indicazione dell'intento.
    6. Domande frequenti suggerite (FAQ).
    7. Suggerimenti per elementi multimediali e call-to-action.
    8. Indicazioni per schema markup e ottimizzazioni on-page specifiche.

    Rispondi in formato Markdown ben strutturato.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Sei un consulente SEO esperto che crea outline strategici completi.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [{"type": "text", "text": user_prompt}],
            },
        ],
        temperature=0.6,
    )
    return response.output_text


def main() -> None:
    st.set_page_config(page_title="SEO Prompt Generator", layout="wide")
    st.title("SEO Prompt Generator con DataForSEO e OpenAI")
    st.write(
        "Crea outline ottimizzati per i motori di ricerca a partire da una query target, "
        "analizzando automaticamente i competitor e generando suggerimenti con OpenAI."
    )

    with st.sidebar:
        st.header("Credenziali API")
        dataforseo_login = st.text_input("DataForSEO Login", type="default")
        dataforseo_password = st.text_input("DataForSEO Password", type="password")
        openai_api_key = st.text_input("OpenAI API Key", type="password")
        st.caption(
            "Le credenziali vengono utilizzate solo localmente per le chiamate API e non vengono salvate."
        )

        st.header("Impostazioni Analisi")
        location_name = st.text_input("Località", value="Italy")
        language_name = st.text_input("Lingua", value="Italian")
        serp_limit = st.slider("Numero di risultati SERP", min_value=3, max_value=20, value=10)
        device = st.selectbox("Dispositivo", ["desktop", "mobile"])

    st.subheader("Query da analizzare")
    keyword = st.text_input("Parola chiave o query principale")
    tone = st.text_input("Tono di voce desiderato", value="Professionale e autorevole")
    audience = st.text_input("Pubblico target", value="Responsabili marketing e content strategist")
    additional_notes = st.text_area("Note aggiuntive")

    if st.button("Genera spunti SEO", type="primary"):
        if not all([keyword, dataforseo_login, dataforseo_password, openai_api_key]):
            st.error(
                "Per procedere sono necessari query, credenziali DataForSEO e API key di OpenAI."
            )
            st.stop()

        with st.spinner("Recupero dei risultati SERP da DataForSEO…"):
            try:
                serp_results = fetch_serp_results(
                    keyword=keyword,
                    location_name=location_name,
                    language_name=language_name,
                    limit=serp_limit,
                    login=dataforseo_login,
                    password=dataforseo_password,
                    device=device,
                )
            except Exception as error:  # noqa: BLE001
                st.error(f"Errore durante il recupero della SERP: {error}")
                st.stop()

        if not serp_results:
            st.warning("Nessun risultato SERP trovato per la query specificata.")
            st.stop()

        st.success("Risultati SERP recuperati.")
        st.write("### Top risultati SERP")
        for result in serp_results:
            st.markdown(
                f"**{result.position}. [{result.title}]({result.url})**\\n"
                f"Snippet: {result.snippet or 'N/A'}"
            )

        with st.spinner("Analisi contenuti competitor…"):
            competitor_brief = build_competitor_brief(serp_results)

        st.write("### Insight dai competitor")
        st.markdown(competitor_brief or "Nessun contenuto disponibile")

        with st.spinner("Generazione outline con OpenAI…"):
            client = OpenAI(api_key=openai_api_key)
            try:
                seo_prompt = generate_seo_prompts(
                    client=client,
                    query=keyword,
                    location=location_name,
                    language=language_name,
                    serp_overview=serp_results,
                    competitor_brief=competitor_brief,
                    tone=tone,
                    audience=audience,
                    additional_notes=additional_notes,
                )
            except Exception as error:  # noqa: BLE001
                st.error(f"Errore durante la generazione con OpenAI: {error}")
                st.stop()

        st.write("### Spunti ottimizzati per la SEO")
        st.markdown(seo_prompt)

        st.download_button(
            "Scarica outline in Markdown",
            data=seo_prompt,
            file_name=f"outline_seo_{keyword.replace(' ', '_')}.md",
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()
