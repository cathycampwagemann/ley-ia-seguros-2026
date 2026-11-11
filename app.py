import streamlit as st
import json, io
from docx import Document
from docx.shared import Pt, Cm

st.set_page_config(page_title="Congreso Extraordinario | Ley IA y Seguros",page_icon="⚖️",layout="wide")
with open("articulos.json",encoding="utf-8") as f: ART=json.load(f)

st.markdown("""<style>
.stApp {background:#081426;color:#f4f7ff}
h1,h2,h3 {color:#f4f7ff!important}
[data-testid="stSidebar"] {background:#10223c}
.eyebrow {letter-spacing:.22em;color:#80d7ec;font-size:.85rem;text-transform:uppercase}
.hero {text-align:center;padding:1.6rem 0 2rem;border-bottom:1px solid #34516c}
.hero h1 {font-size:clamp(2rem,4vw,4.1rem);line-height:1.12;margin:.6rem 0;color:#fff}
.hero p {color:#c1d5e8;font-size:1.1rem}
.article {background:#11243d;border:1px solid #2e5274;border-radius:16px;padding:1.25rem 1.7rem;margin:1rem 0}
.article h2 {font-size:1.35rem;margin:0 0 .75rem;color:#8bdfee!important}
.article p {font-size:1.18rem;line-height:1.65;color:#fff;margin:0}
.footer {text-align:center;color:#9ebbd0;padding:2rem}
</style>""",unsafe_allow_html=True)

if 'choices' not in st.session_state: st.session_state.choices={}
params=st.query_params
for a in ART:
 k=str(a['number']);v=params.get('a'+k)
 if v in 'ABCD' if v else False: st.session_state.choices[k]=v

with st.sidebar:
 st.header('Mesa de votación')
 st.caption('Selecciona la alternativa ganadora de cada artículo. No se muestran porcentajes.')
 for a in ART:
  k=str(a['number']); opts=['—','A','B','C','D'];cur=st.session_state.choices.get(k,'—')
  selected=st.selectbox(f'Artículo {k}',opts,index=opts.index(cur),key='selector_'+k)
  if selected=='—':st.session_state.choices.pop(k,None)
  else:st.session_state.choices[k]=selected
 if st.button('Actualizar texto aprobado',use_container_width=True):
  st.query_params.update({('a'+k):v for k,v in st.session_state.choices.items()})
  st.rerun()
 st.divider()
 mode=st.toggle('Modo proyección',value=False,help='Oculta las herramientas de edición en la pantalla principal.')
 if mode:st.markdown('Usa la flecha superior izquierda para ocultar la barra lateral; presiona F11 para pantalla completa.')

st.markdown('<div class="hero"><div class="eyebrow">Congreso Extraordinario · 2026</div><h1>Ley de Inteligencia Artificial<br>y Seguros</h1><p>Texto aprobado por el Congreso Extraordinario</p></div>',unsafe_allow_html=True)
chosen=[(a,st.session_state.choices.get(str(a['number']))) for a in ART]
ready=sum(v in ('A','B','C','D') for a,v in chosen)
if ready<7:st.info(f'{ready} de 7 artículos seleccionados. Los artículos pendientes no se proyectan.')
for a,v in chosen:
 if v not in ('A','B','C','D'):continue
 import html
 title=html.escape(a['title']);body=html.escape(a['options'][v])
 st.markdown(f'<div class="article"><h2>ARTÍCULO {a["number"]}° · {title}</h2><p>{body}</p></div>',unsafe_allow_html=True)

def create_doc():
 d=Document(); sec=d.sections[0];sec.top_margin=Cm(2.4);sec.bottom_margin=Cm(2.4)
 d.add_heading('LEY DE INTELIGENCIA ARTIFICIAL Y SEGUROS',0)
 d.add_paragraph('Congreso Extraordinario 2026')
 for a,v in chosen:
  if v not in ('A','B','C','D'):continue
  d.add_heading(f'Artículo {a["number"]}°: {a["title"]}',level=2)
  d.add_paragraph(a['options'][v])
 buf=io.BytesIO();d.save(buf);return buf.getvalue()
if ready==7:
 st.download_button('Descargar ley aprobada en Word',create_doc(),file_name='Ley_IA_y_Seguros_2026.docx',mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',use_container_width=True)
st.markdown('<div class="footer">Congreso Extraordinario de Inteligencia Artificial y Seguros · 2026</div>',unsafe_allow_html=True)
