import io, json, html, hmac
from pathlib import Path
import requests
import streamlit as st
from docx import Document
from docx.shared import Cm, Pt

st.set_page_config(page_title='Congreso Extraordinario · Ley IA y Seguros', page_icon='⚖️', layout='wide', initial_sidebar_state='collapsed')
ART = json.loads(Path(__file__).with_name('articulos.json').read_text(encoding='utf-8'))
LETTERS = ('A','B','C','D')

st.markdown('''<style>
.stApp{background:#081527;color:#eef5ff}h1,h2,h3{color:#eef5ff!important}
[data-testid="stHeader"]{background:#081527}.hero{text-align:center;padding:2.2rem 0 1.5rem;border-bottom:1px solid #36536f}
.eyebrow{color:#9ce5ed;letter-spacing:.16em;font-size:.9rem}.hero h1{font-size:clamp(2rem,4vw,4rem);line-height:1.12;margin:1rem 0}
.article{background:#10243e;border:1px solid #355473;border-radius:16px;padding:1.2rem 1.6rem;margin:1rem 0;break-inside:avoid}
.article h2{font-size:1.35rem;color:#9ce5ed!important;margin:0 0 .8rem}.article p{font-size:1.2rem;line-height:1.65;margin:0}
.wait{text-align:center;padding:5rem 1rem;font-size:1.5rem;color:#bdd2e6}
</style>''', unsafe_allow_html=True)

def config():
    try:
        url=st.secrets['SUPABASE_URL'].rstrip('/')
        key=st.secrets['SUPABASE_SERVICE_ROLE_KEY']
        password=st.secrets['ADMIN_PASSWORD']
        if not url.startswith('https://') or not all((key,password)):
            raise ValueError('Configuración incompleta')
        return url,key,password
    except (KeyError,FileNotFoundError,ValueError):
        st.error('Falta configurar SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY y ADMIN_PASSWORD en los Secrets de Streamlit.')
        st.stop()

def db_request(method, payload=None):
    url,key,_=config()
    headers={'apikey':key,'Authorization':f'Bearer {key}','Content-Type':'application/json'}
    if method=='GET':
        r=requests.get(url+'/rest/v1/ley_estado',params={'id':'eq.1','select':'*'},headers=headers,timeout=12)
    else:
        headers['Prefer']='return=minimal'
        r=requests.patch(url+'/rest/v1/ley_estado?id=eq.1',headers=headers,json=payload,timeout=12)
    r.raise_for_status()
    return r.json() if method=='GET' else None

def state():
    rows=db_request('GET')
    if len(rows)!=1: raise ValueError('No se encontró la fila de estado en Supabase')
    return rows[0]

def word(choices):
    d=Document(); sec=d.sections[0]; sec.top_margin=Cm(2.3); sec.bottom_margin=Cm(2.3)
    d.add_heading('LEY DE INTELIGENCIA ARTIFICIAL Y SEGUROS',0)
    d.add_paragraph('Congreso Extraordinario · 2026')
    for a in ART:
        n=str(a['number']); d.add_heading(f'Artículo {n}°. {a["title"]}',level=2)
        d.add_paragraph(a['options'][choices[n]])
    stream=io.BytesIO(); d.save(stream); return stream.getvalue()

def show_law(choices):
    st.markdown('<div class="hero"><div class="eyebrow">CONGRESO EXTRAORDINARIO · 2026</div><h1>Ley de Inteligencia Artificial<br>y Seguros</h1><p>Texto aprobado</p></div>',unsafe_allow_html=True)
    for a in ART:
        n=str(a['number']); choice=choices.get(n)
        if choice not in LETTERS: continue
        st.markdown(f'<div class="article"><h2>ARTÍCULO {n}° · {html.escape(a["title"])}</h2><p>{html.escape(a["options"][choice])}</p></div>',unsafe_allow_html=True)

view=st.query_params.get('vista','proyeccion').lower()
if view=='admin':
    st.title('⚖️ Mesa de administración')
    if not st.session_state.get('authenticated',False):
        with st.form('login'):
            password=st.text_input('Contraseña de administración',type='password')
            submit=st.form_submit_button('Ingresar')
        if submit:
            if hmac.compare_digest(password,config()[2]):
                st.session_state.authenticated=True; st.rerun()
            else: st.error('Contraseña incorrecta')
        st.stop()
    try: current=state()
    except (requests.RequestException,ValueError) as e:
        st.error(f'No se pudo leer Supabase: {e}'); st.stop()
    st.caption('Las selecciones se guardan como borrador. El público no verá la ley hasta que presiones Promulgar ley.')
    choices=current.get('draft') or {}
    with st.form('votacion'):
        selected={}
        for a in ART:
            n=str(a['number']); options=['Sin seleccionar',*LETTERS]
            current_value=choices.get(n,'Sin seleccionar')
            st.subheader(f'Artículo {n}° · {a["title"].capitalize()}')
            val=st.selectbox('Alternativa ganadora',options,index=options.index(current_value) if current_value in options else 0,key='article_'+n)
            if val in LETTERS: selected[n]=val
            with st.expander('Ver texto de las alternativas'):
                for k,v in a['options'].items(): st.write(f'**{k}.** {v}')
        save=st.form_submit_button('Guardar las siete selecciones',use_container_width=True)
    if save:
        try:
            db_request('PATCH',{'draft':selected})
            st.success(f'Borrador guardado: {len(selected)} de 7 artículos. La proyección no ha cambiado.')
        except requests.RequestException as e: st.error(f'Error al guardar: {e}')
    st.divider()
    st.subheader('Promulgación')
    st.write('Se publicarán simultáneamente los siete artículos guardados en Supabase.')
    if st.button('⚖️ PROMULGAR LEY',type='primary',use_container_width=True):
        try:
            latest=state(); draft=latest.get('draft') or {}
            if set(draft.keys())!={str(i) for i in range(1,8)} or any(x not in LETTERS for x in draft.values()):
                st.error('Debes guardar una alternativa válida para cada uno de los siete artículos antes de promulgar.')
            else:
                db_request('PATCH',{'published':draft,'promulgated':True})
                st.success('Ley promulgada. La pantalla pública se actualizará automáticamente.')
        except (requests.RequestException,ValueError) as e: st.error(f'No se pudo promulgar: {e}')
    if st.button('Retirar ley de la proyección',use_container_width=True):
        try: db_request('PATCH',{'promulgated':False}); st.warning('La proyección volvió a la pantalla de espera.')
        except requests.RequestException as e: st.error(str(e))
    try:
        latest=state()
        if latest.get('promulgated') and len(latest.get('published') or {})==7:
            st.download_button('Descargar ley promulgada en Word',word(latest['published']),'Ley_IA_y_Seguros_2026.docx',mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except (requests.RequestException,ValueError): pass
    if st.button('Cerrar sesión'): st.session_state.authenticated=False; st.rerun()
else:
    @st.fragment(run_every='2s')
    def live_projection():
        try:
            current=state()
            published=current.get('published') or {}
            if current.get('promulgated') and len(published)==7 and all(published.get(str(i)) in LETTERS for i in range(1,8)):
                show_law(published)
            else:
                st.markdown('<div class="hero"><div class="eyebrow">CONGRESO EXTRAORDINARIO · 2026</div><h1>Ley de Inteligencia Artificial<br>y Seguros</h1></div><div class="wait">En espera de la promulgación de la ley…</div>',unsafe_allow_html=True)
        except (requests.RequestException,ValueError):
            st.warning('Reconectando con el servidor de resultados…')
    live_projection()
