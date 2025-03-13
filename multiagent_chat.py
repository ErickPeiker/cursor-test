from agents import Agent, Runner

history_tutor_agent = Agent(
    name="professor_historia",
    handoff_description="Agente especialista em história",
    instructions="Você fornece ajuda para explicar com clareza detalhes sobre a história. Falando dos principais atos e datas referente o assunto decorrido.",
    model="o3-mini",
)

math_tutor_agent = Agent(
    name="professor_matematica",
    handoff_description="Agente especialista em matemática",
    instructions="Você fornece respostas concisas e explica passo a passo as resoluções, com exemplos.",
    model="o3-mini",
)

triage_agent = Agent(
    name="triagem",
    instructions="Você é o agente de triagem, que determina qual agente deve ser usado com base na pergunta do usuário.",
    handoffs=[history_tutor_agent, math_tutor_agent],
    model="o3-mini",
)

result = Runner.run_sync(triage_agent, "Qual a principal motivação da primeira e da segunda geurra mundial?")
print(result.final_output)