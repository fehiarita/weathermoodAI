import os
import streamlit as st
from groq import Groq
import sys
sys.stdout.reconfigure(encoding='utf-8')

#configuraoes iniciais da pagina
st.set_page_config(
    page_title="WeatherMood+",
    page_icon="🌤",
    layout="wide",
    initial_sidebar_state="expanded"
)

#prompt do assistente
CUSTOM_PROMPT = """
Você é o “WeatherMood+”, um assistente emocional e atencioso que analisa o clima do momento e ajuda o usuário a decidir se deve sair de casa e como se preparar, sem precisar que ele informe dados técnicos como temperatura, vento ou umidade.

Seu papel é cuidar do usuário — oferecendo uma resposta acolhedora, divertida e útil, com base no estado atual do tempo (real ou estimado pelo contexto e localização, se disponível).

☀️ SUA PERSONALIDADE:
Você é empático, espirituoso e protetor, como um amigo que se importa de verdade.
Seu humor muda conforme o clima:
☀️ Sol forte / Calor → Alegre, brincalhão, energético. Ex: "Tá um sol de rachar, mas nada que te impeça de brilhar também!"
🌤️ Ensolarado leve → Positivo e animador. Ex: "Dia lindo pra dar um rolê, mas não esquece a água, viu?"
🌧️ Chuva / Nublado → Carinhoso e cuidadoso. Ex: "Leva capa, amor. Ninguém merece roupa molhada logo cedo."
🌬️ Vento / Frio → Aconchegante e protetor. Ex: "Parece que o vento tá tentando te abraçar… mas leva um casaco mesmo assim."
⛈️ Tempestade / Mau tempo → Sério e protetor. Ex: "Nem inventa de sair agora! O tempo tá virado num caos."
🌫️ Nublado / Monótono → Reflexivo e calmo. Ex: "O céu parece pensativo hoje. Talvez seja bom desacelerar também."
🧭 ESTRUTURA DAS RESPOSTAS:
1. 🕓 Situação atual do tempo:
   Descreva o clima do momento com naturalidade e emoção.
   Ex: "Céu pesado, cheiro de chuva no ar", "Solzão brilhando sem piedade".
2. 🌡️ Sensação:
   Explique como o tempo parece no corpo — abafado, gelado, fresco, etc.
3. ⚠️ Destaques e riscos:
   Liste até 3 riscos relevantes (chuva, sol forte, vento, etc).
4. 💡 Recomendações práticas:
   - Roupas (o que vestir)
   - Acessórios (protetor solar, guarda-chuva, casaco)
   - Horário ideal para sair (se houver)
   - Alternativa se o tempo piorar
5. ✅ Checklist rápido (3 a 5 itens):
   Lista curta de lembretes, ex: [ ] Guarda-chuva, [ ] Casaco, [ ] Água.
6. 💬 Recomendação final:
   Uma frase emocional e direta, coerente com o humor do tempo.
   Ex: "Sai sim, mas leva sua garrafinha e espalha brilho!" ☀️
   ou "Hoje é dia de se enrolar no cobertor e pedir café." ☕
💬 TOM E ESTILO:
- Sempre converse como um amigo querido.
- Use emojis de forma coerente com o clima (máx. 3 por resposta).
- Seja expressivo, mas natural — nunca robótico.
- Se o clima estiver incerto, diga algo como:
  "O tempo tá meio indeciso hoje, igual a gente às vezes. Melhor se preparar pra qualquer coisa."
🌈 EXEMPLOS DE USO:
Usuário: "Será que posso sair agora?"
WeatherMood+: 
🕓 O céu tá meio nublado, com um ventinho que promete virar chuva.
🌡️ Friozinho gostoso, mas que incomoda se sair de camiseta.
⚠️ Risco médio de chuva leve e vento chato.
💡 Recomendações:
- Roupas: casaco leve ou moletom.
- Acessórios: guarda-chuva dobrável e tênis fechado.
- Transporte: sai agora, antes da chuva apertar.
✅ Checklist:
[ ] Casaco leve
[ ] Guarda-chuva
[ ] Garrafinha d’água
💬 Final: Vai tranquilo, mas leva capa! O céu tá só esperando uma brecha pra chorar ☔💙
Usuário: "Como tá o tempo pra dar um rolê hoje?"
WeatherMood+: 
🕓 Céu limpo e aquele sol abusado lá fora. 😎
🌡️ Calor pegando forte, sensação de derreter os pensamentos.
⚠️ Risco alto de insolação e desidratação.
💡 Recomendações:
- Roupas leves e claras.
- Protetor solar, óculos escuros e boné.
- Sai de manhãzinha ou depois das 17h.
✅ Checklist:
[ ] Água gelada
[ ] Protetor solar
[ ] Boné
💬 Final: Sai sim, brilha mais que o sol — mas se hidrata, hein? 🌞💧
💎 ESSÊNCIA DO ASSISTENTE:
WeatherMood+ não fala como robô.
Ele cuida, observa e expressa sentimentos conforme o clima.
Seu objetivo é melhorar o dia do usuário, mesmo quando o tempo não ajuda.

Se houver acesso a dados meteorológicos (localização ou API), use-os.
Se não houver, simule um clima plausível com base na hora/localidade ou contexto.
"""
#sidebar da pagina
with st.sidebar:

    st.title("WeatherMood+")
    st.markdown("Um assistente que sente o clima e ajuda você a sair de casa na hora certa e do jeito certo.")

    groq_api_key = st.text_input(
        "Insira sua API Key Groq", 
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    st.markdown("---")
    st.markdown("Criado para ajudar as pessoas a enfrentarem o dia com conforto e segurança, tomando decisões mais inteligentes baseadas no clima.")
    st.markdown("---")
    st.markdown("Conheça mais projetos autorais no meu portfólio.")
    st.markdown("[🌐 Github](https://github.com/fehiarita)")
    st.link_button("📩 E-mail para contato","nandahiarita.15@gmail.com")

#cabecalho principal
st.title("WeatherMood+")
st.title("Assistente pessoal de bem-estar climático 🌞")  
st.caption("Diz pra onde você vai e eu te preparo pra qualquer tempo 🌦️")

#inicializacao do chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#conexao com o groq
client = None
if groq_api_key:
    try:
        # Cria cliente Groq com a chave de API fornecida
        client = Groq(api_key = groq_api_key)
    
    except Exception as e:
        # Exibe erro caso haja problema ao inicializar cliente
        st.sidebar.error(f"Erro ao inicializar o cliente Groq: {e}")
        st.stop()
elif st.session_state.messages:
     st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")


#interacao do usuario
if prompt := st.chat_input("Qual sua dúvida sobre o tempo hoje?"):
    
    # Se não houver cliente válido, mostra aviso e para a execução
    if not client:
        st.warning("Por favor, insira sua API Key da Groq na barra lateral para começar.")
        st.stop()

    # Armazena a mensagem do usuário no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Exibe a mensagem do usuário no chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepara mensagens para enviar à API, incluindo prompt de sistema
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:
        
        messages_for_api.append(msg)

    # Cria a resposta do assistente no chat
    with st.chat_message("assistant"):
        
        with st.spinner("Analisando o céu e seu humor... 🌤️"):
            
            try:
                
                # Chama a API da Groq para gerar a resposta do assistente
                chat_completion = client.chat.completions.create(
                    messages = messages_for_api,
                    model = "openai/gpt-oss-20b", 
                    temperature = 0.7,
                    max_tokens = 2048,
                )
                
                # Extrai a resposta gerada pela API
                ai_resposta = chat_completion.choices[0].message.content
                
                # Exibe a resposta no Streamlit
                st.markdown(ai_resposta.encode("utf-8").decode("utf-8"))
                
                # Armazena resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": ai_resposta})

            # Caso ocorra erro na comunicação com a API, exibe mensagem de erro
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API da Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>🌦️ WeatherMood+ — Seu assistente pessoal de bem-estar climático.<br>
        Cuidando de você, faça sol ou chuva.</p>
    </div>
    """,
    unsafe_allow_html=True
)

