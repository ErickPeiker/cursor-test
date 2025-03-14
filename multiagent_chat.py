import aiohttp
import asyncio
from agents import Agent, Runner, WebSearchTool, function_tool

@function_tool  
async def fetch_weather(location: str) -> str:
    api_key = "5c1899349eca44ce84f222340251303"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&lang=pt"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
        
        if "error" in data:
            return f"Erro ao obter a previsão do tempo: {data['error']['message']}"
        
        weather = data['current']
        return (
            f"Tempo atual em {location}:\n"
            f"🌡️ Temperatura: {weather['temp_c']}°C\n"
            f"💧 Umidade: {weather['humidity']}%\n"
            f"🌬️ Vento: {weather['wind_kph']} km/h\n"
            f"⛅ Condição: {weather['condition']['text']}"
        )
    except Exception as e:
        return f"Erro ao buscar a previsão do tempo: {str(e)}"

# Definir o agente meteorológico
weather_agent = Agent(
    name="weather_agent",
    handoff_description="Agente especialista em previsão do tempo.",
    instructions="Você captura a localização que o usuário informou e responde perguntas sobre previsão do tempo exatamente como a tool fetch_weather retornar.",
    tools=[fetch_weather],
    model="o3-mini",
)

fallback_agent = Agent(
    name="fallback_agent",
    handoff_description="Agente de fallback para perguntas escolares que não se encaixam nas categorias existentes.",
    instructions="Você lida com perguntas que não se encaixam nas categorias existentes nas matérias de escola primária. Solicite ao usuário para reformular a pergunta e reforce quais são as categorias disponíveis.",
    model="o3-mini",
)

web_agent = Agent(
    name="web_agent",
    instructions="Você é um agente que busca informações na web.",
    tools=[
        WebSearchTool(),
    ],
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

triage_agent = Agent(
    name="triagem",
    instructions=(
        "Você determina qual agente usar com base na pergunta do usuário: "
        "matemática para professor_matematica, "
        "previsão do tempo para weather_agent, "
        "história para professor_historia, "
        "somente quando pedir para pesquisar na internet vai para o web_agent, "        
        "e caso não se enquadre nessas categorias use o fallback_agent."
    ),
    handoffs=[fallback_agent, web_agent, history_tutor_agent, math_tutor_agent, weather_agent],
    model="o3-mini",
)

async def main():
    result = await Runner.run(triage_agent, "Como que faço cálculo de raiz quadrada?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
