import streamlit as st
import yfinance as yf
import pandas as pd
import os
import plotly.express as px


# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="ESG Dashboard",
    page_icon="🌱",
    layout="wide"
)


# =====================================================
# TITRE
# =====================================================

st.title("🌱 Tableau de bord ESG")

st.write(
    "Analyse environnementale, sociale et de gouvernance "
    "d'une entreprise."
)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("🔎 Entreprise")

ticker_input = st.sidebar.text_input(
    "Ticker de l'entreprise",
    value="AAPL"
)

analyser = st.sidebar.button("Analyser")


# =====================================================
# ANALYSE
# =====================================================

if analyser:

    ticker_symbol = ticker_input.upper().strip()

    if not ticker_symbol:
        st.error("Veuillez saisir un ticker.")
        st.stop()

    try:

        # =================================================
        # YAHOO FINANCE
        # =================================================

        ticker = yf.Ticker(ticker_symbol)

        info = ticker.info

        company_name = info.get(
            "longName",
            ticker_symbol
        )

        sector = info.get(
            "sector",
            "Non disponible"
        )

        industry = info.get(
            "industry",
            "Non disponible"
        )

        employees = info.get(
            "fullTimeEmployees",
            None
        )

        market_cap = info.get(
            "marketCap",
            None
        )

        revenue = info.get(
            "totalRevenue",
            None
        )


        # =================================================
        # ENTREPRISE
        # =================================================

        st.header(company_name)

        st.write(
            f"**Ticker :** {ticker_symbol}"
        )

        st.write(
            f"**Secteur :** {sector}"
        )

        st.write(
            f"**Industrie :** {industry}"
        )


        # =================================================
        # INFORMATIONS GÉNÉRALES
        # =================================================

        st.subheader(
            "📊 Informations générales"
        )

        col1, col2, col3 = st.columns(3)


        # -------------------------------------------------
        # CAPITALISATION
        # -------------------------------------------------

        with col1:

            if market_cap is not None:

                market_cap_billions = (
                    market_cap / 1_000_000_000
                )

                st.metric(
                    "Capitalisation",
                    f"{market_cap_billions:.1f} Md $"
                )

            else:

                st.metric(
                    "Capitalisation",
                    "N/A"
                )


        # -------------------------------------------------
        # CHIFFRE D'AFFAIRES
        # -------------------------------------------------

        with col2:

            if revenue is not None:

                revenue_billions = (
                    revenue / 1_000_000_000
                )

                st.metric(
                    "Chiffre d'affaires",
                    f"{revenue_billions:.1f} Md $"
                )

            else:

                st.metric(
                    "Chiffre d'affaires",
                    "N/A"
                )


        # -------------------------------------------------
        # EMPLOYÉS
        # -------------------------------------------------

        with col3:

            if employees is not None:

                st.metric(
                    "Employés",
                    f"{employees:,}"
                )

            else:

                st.metric(
                    "Employés",
                    "N/A"
                )


        # =================================================
        # CHARGEMENT DES DONNÉES ESG
        # =================================================

        st.divider()

        st.header(
            "🌱 Analyse ESG"
        )

        esg_file = os.path.join(
            "data",
            "apple_esg.csv"
        )


        if os.path.exists(esg_file):

            esg_data = pd.read_csv(
                esg_file
            )

        else:

            st.error(
                "Le fichier data/apple_esg.csv "
                "est introuvable."
            )

            st.stop()


        # =================================================
        # HISTORIQUE
        # =================================================

        history_file = os.path.join(
            "data",
            "esg_history.csv"
        )


        if os.path.exists(history_file):

            history_data = pd.read_csv(
                history_file
            )

        else:

            history_data = pd.DataFrame()


        # =================================================
        # ENVIRONNEMENT
        # =================================================

        st.subheader(
            "🌱 Environnement"
        )

        environmental = esg_data[
            esg_data["pilier"] == "E"
        ]


        if not environmental.empty:

            columns = st.columns(3)

            for i, (_, row) in enumerate(
                environmental.iterrows()
            ):

                with columns[i % 3]:

                    valeur = row["valeur"]
                    unite = row["unite"]
                    indicateur = row["indicateur"]


                    if unite == "%":

                        affichage = (
                            f"{valeur} %"
                        )

                    elif unite == "personnes":

                        affichage = (
                            f"{int(valeur):,}"
                        )

                    else:

                        affichage = (
                            f"{valeur} {unite}"
                        )


                    st.metric(
                        indicateur,
                        affichage
                    )

        else:

            st.info(
                "Aucune donnée environnementale "
                "disponible."
            )


        # =================================================
        # SOCIAL
        # =================================================

        st.subheader(
            "👥 Social"
        )

        social = esg_data[
            esg_data["pilier"] == "S"
        ]


        if not social.empty:

            columns = st.columns(3)

            for i, (_, row) in enumerate(
                social.iterrows()
            ):

                with columns[i % 3]:

                    valeur = row["valeur"]
                    unite = row["unite"]
                    indicateur = row["indicateur"]


                    if unite == "%":

                        affichage = (
                            f"{valeur} %"
                        )

                    elif unite == "personnes":

                        if valeur >= 1_000_000:

                            affichage = (
                                f"{valeur / 1_000_000:.1f} M"
                            )

                        elif valeur >= 1_000:

                            affichage = (
                                f"{valeur / 1_000:.0f} k"
                            )

                        else:

                            affichage = (
                                f"{int(valeur)}"
                            )

                    else:

                        affichage = (
                            f"{valeur} {unite}"
                        )


                    st.metric(
                        indicateur,
                        affichage
                    )

        else:

            st.info(
                "Aucune donnée sociale "
                "disponible."
            )


        # =================================================
        # GOUVERNANCE
        # =================================================

        st.subheader(
            "🏛️ Gouvernance"
        )

        governance = esg_data[
            esg_data["pilier"] == "G"
        ]


        if not governance.empty:

            columns = st.columns(3)

            for i, (_, row) in enumerate(
                governance.iterrows()
            ):

                with columns[i % 3]:

                    valeur = row["valeur"]
                    unite = row["unite"]
                    indicateur = row["indicateur"]


                    if unite == "membres":

                        affichage = (
                            f"{int(valeur)}"
                        )

                    elif unite in [
                        "poste",
                        "oui"
                    ]:

                        affichage = "Oui"

                    else:

                        affichage = (
                            f"{valeur} {unite}"
                        )


                    st.metric(
                        indicateur,
                        affichage
                    )

        else:

            st.info(
                "Aucune donnée de gouvernance "
                "disponible."
            )


        # =================================================
        # VISUALISATION ESG
        # =================================================

        st.divider()

        st.subheader(
            "📊 Visualisation ESG"
        )


        pilier_selectionne = st.selectbox(
            "Sélectionner un pilier",
            ["Tous", "E", "S", "G"]
        )


        if pilier_selectionne == "Tous":

            graph_data = esg_data.copy()

        else:

            graph_data = esg_data[
                esg_data["pilier"]
                == pilier_selectionne
            ].copy()


        if not graph_data.empty:

            graph_data["libelle"] = (
                graph_data["indicateur"]
                + " ("
                + graph_data["unite"]
                + ")"
            )


            fig = px.bar(
                graph_data,
                x="valeur",
                y="libelle",
                color="pilier",
                orientation="h",
                title="Indicateurs ESG",
                labels={
                    "valeur": "Valeur",
                    "libelle": "Indicateur",
                    "pilier": "Pilier"
                }
            )


            fig.update_layout(
                height=550,
                yaxis={
                    "categoryorder":
                    "total ascending"
                }
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Aucune donnée disponible "
                "pour ce pilier."
            )


        # =================================================
        # HISTORIQUE ESG
        # =================================================

        st.divider()

        st.subheader(
            "📈 Évolution historique"
        )


        if not history_data.empty:

            # Liste des indicateurs
            indicateurs = sorted(
                history_data[
                    "indicateur"
                ]
                .dropna()
                .unique()
            )


            if len(indicateurs) > 0:

                indicateur_selectionne = (
                    st.selectbox(
                        "Choisir un indicateur",
                        indicateurs
                    )
                )


                # Filtrer
                history_filtered = (
                    history_data[
                        history_data[
                            "indicateur"
                        ]
                        == indicateur_selectionne
                    ]
                    .copy()
                )


                # Trier par année
                history_filtered = (
                    history_filtered
                    .sort_values("annee")
                )


                if not history_filtered.empty:

                    # Unité
                    unite = (
                        history_filtered[
                            "unite"
                        ].iloc[0]
                    )


                    # Graphique
                    fig_history = px.line(
                        history_filtered,
                        x="annee",
                        y="valeur",
                        markers=True,
                        title=(
                            "Évolution : "
                            + indicateur_selectionne
                        ),
                        labels={
                            "annee": "Année",
                            "valeur": unite
                        }
                    )


                    fig_history.update_traces(
                        line=dict(
                            width=3
                        ),
                        marker=dict(
                            size=10
                        )
                    )


                    fig_history.update_layout(
                        height=450,
                        hovermode="x unified"
                    )


                    st.plotly_chart(
                        fig_history,
                        use_container_width=True
                    )


                    st.caption(
                        f"Unité : {unite}"
                    )


                    # Données utilisées
                    with st.expander(
                        "📋 Voir les données utilisées"
                    ):

                        st.dataframe(
                            history_filtered,
                            use_container_width=True,
                            hide_index=True
                        )

                else:

                    st.info(
                        "Aucune donnée disponible "
                        "pour cet indicateur."
                    )

            else:

                st.info(
                    "Aucun indicateur historique "
                    "disponible."
                )

        else:

            st.info(
                "Aucune donnée historique "
                "disponible."
            )


        # =================================================
        # TABLEAU DES DONNÉES
        # =================================================

        st.divider()

        st.subheader(
            "📋 Données ESG"
        )


        st.dataframe(
            esg_data,
            use_container_width=True,
            hide_index=True
        )


        # =================================================
        # SOURCES
        # =================================================

        st.subheader(
            "📚 Sources"
        )

        st.write(
            "Les sources des indicateurs sont "
            "indiquées dans la colonne "
            "'source' du tableau."
        )


    # =====================================================
    # GESTION DES ERREURS
    # =====================================================

    except Exception as e:

        st.error(
            f"Erreur lors de l'analyse : {e}"
        )



