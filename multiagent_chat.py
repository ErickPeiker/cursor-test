from agents import Agent, Runner, WebSearchTool

fallback_agent = Agent(
    name="fallback_agent",
    handoff_description="Agente de fallback para perguntas escolares que não se encaixam nas categorias existentes.",
    instructions="Você lida com perguntas que não se encaixam nas categorias existentes nas matérias de escola primária. Solicite ao usuário para reformular a pergunta e reforce quais são as categorias disponíveis.",
    model="o3-mini",
)

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

web_agent = Agent(
    name="web_agent",
    instructions="Você é um agente que busca informações na web.",
    tools=[
        WebSearchTool(),
    ],
)

triage_agent = Agent(
    name="triagem",
    instructions="Você é o agente de triagem, que determina qual agente deve ser usado com base na pergunta do usuário.",
    handoffs=[fallback_agent, history_tutor_agent, math_tutor_agent, web_agent],
    model="o3-mini",
)

result = Runner.run_sync(triage_agent, "Quanto custa uma bolsa?")
print(result.final_output)