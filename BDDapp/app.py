import streamlit as st
import pandas as pd
import plotly.express as px
from dbfct import creer_table, ajout_data, voir_data, voir_unique_texte, get_texte, edit_texte_data

def main():
	st.title("BDD App")

	menu = ["Créer", "Lire", "Mettre à jour", "Supprimer", "A propos"]
	choice = st.sidebar.selectbox("Menu", menu)

	creer_table()
	if choice == "Créer":
		st.subheader("Ajouter des élements")


		col1, col2 = st.columns(2)

		with col1:
			texte = st.text_area("ajouter un texte")

		with col2:
			etat = st.selectbox("état", ["Fait", "En cours", "Pas fait"])
			date_etat = st.date_input("Date")


		if st.button("Ajouter données"):
			ajout_data(texte, etat, date_etat)
			st.success("Les données ont bien été ajoutés :{}".format(texte))

	elif choice == "Lire":
		st.subheader("Lecture")
		resultat = voir_data()
		df = pd.DataFrame(resultat, columns=['texte', 'etat', 'date'])
		with st.expander("Voir toutes les données"):
			st.dataframe(df)

		with st.expander('Etat'):
			texte_df = df['etat'].value_counts().to_frame()
			
			texte_df = texte_df.reset_index()
			st.dataframe(texte_df)

			p1 = px.pie(texte_df,names='index',values='etat')
			st.plotly_chart(p1)


	elif choice == "Mettre à jour":
		st.subheader("Mettre à jour les données")
		resultat = voir_data()
		df = pd.DataFrame(resultat, columns=['texte', 'etat', 'date'])
		with st.expander("Données actuelles"):
			st.dataframe(df)

		#st.write(voir_unique_texte())
		list_texte = [i[0] for i in voir_unique_texte()]
		#st.write(list_texte)

		texte_selectionne = st.selectbox("Texte à éditer", list_texte)

		resultat_selectionne = get_texte(texte_selectionne)
		st.write(resultat_selectionne)
		if resultat_selectionne:
			texte = resultat_selectionne[0][0]
			texte_etat = resultat_selectionne[0][1]
			texte_date = resultat_selectionne[0][2]
			col1, col2 = st.columns(2)

		with col1:
			new_texte = st.text_area("ajouter un texte")

		with col2:
			new_etat = st.selectbox(texte_etat, ["Fait", "En cours", "Pas fait"])
			new_date_etat = st.date_input(texte_date)


		if st.button("Mettre à jour données"):
			edit_texte_data(new_texte, new_etat, new_date_etat, texte, etat, date_etat)
			st.success("Les données ont bien été mise à jour :{}".format(texte, new_texte))





	elif choice == "Supprimer":
		st.subheader("Supprimer des élements")

	else:
		st.subheader("A propos")




if __name__== '__main__':
	main()