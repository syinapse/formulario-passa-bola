const title = document.getElementById('inputTitle')
const mainTitle = document.getElementById('mainTitle')
const btnClean = document.getElementById('btnClean')

const inputEventDateStart = document.getElementById('inputEventDateStart')
const inputAddressEvent = document.getElementById('inputAddressEventDate')
const inputDateEventEnd = document.getElementById('inputDateEventEnd')
const selectState = document.getElementById('selectState')
const inputWhatsapp = document.getElementById('inputWhatsapp')
const inputEventDescription = document.getElementById('inputEventDescription')
const inputEventReward = document.getElementById('inputEventReward')
const inputMinAge = document.getElementById('inputMinAge')
const inputMaxAge = document.getElementById('inputMaxAge')
const inputMaxTotalUni = document.getElementById('inputMaxTotalUni')
const inputMaxTotalTeam = document.getElementById('inputMaxTotalTeam')
const inputCostUni = document.getElementById('inputCostUni')
const inputCostTeam = document.getElementById('inputCostTeam')
const inputLinkedin = document.getElementById('inputLinkedin')
const inputInstagram = document.getElementById('inputInstagram')
const inputOther = document.getElementById('inputOther')
const btnAuto = document.getElementById('btnAuto-fill')

const handlerInputOnChange = function(e) {
    mainTitle.innerText = !title.value ? "Meu Novo evento" : e.target.value;
}

const handlerDefaultInput = function(e) {
    const date_now = new Date()
    title.value = 'Copa Passa a Bola'
    mainTitle.innerText = title.value
    inputEventDateStart.value = `${date_now.getMonth()}-${date_now.getDate()}-${date_now.getFullYear()}`
    inputDateEventEnd.value = `${date_now.getMonth()}-${date_now.setDate(date_now.getDate() + 10)}-${date_now.getFullYear()}`
    inputAddressEvent.value = 'Vila Mariana 233'
    selectState.value = 'sp'
    inputWhatsapp.value = '11987654321'
    inputEventDescription.value = `A Copa Passa a Bola é mais do que um torneio: é uma celebração da força, talento e paixão das mulheres no futebol. Em sua segunda edição, queremos descobrir novos talentos, fortalecer a comunidade e oferecer uma experiência única de competição, visibilidade e oportunidade. Traga seu time ou inscreva-se individualmente e venha fazer história! 
    

    Sobre o Campeonato

    A Copa Passa a Bola 2025 é um torneio de Futebol de Campo (11 jogadoras) voltado para atletas amadoras acima de 16 anos. O objetivo é promover integração, revelar talentos e criar um ambiente seguro e profissional para a prática do esporte.
    Formato da Competição
        Fase de Grupos: As equipes serão divididas em grupos e jogarão em turno único. As melhores classificadas avançam para a fase eliminatória.
        Fase Eliminatória (mata-mata): Jogos únicos de quartas de final, semifinal e final.
        Local dos Jogos: Campos parceiros na cidade de São Paulo. Os locais exatos serão divulgados após o encerramento das inscrições.
    Categorias de Inscrição
        Inscrição de Time: Equipes já formadas com no mínimo 11 e no máximo 15 jogadoras, mais comissão técnica.
        Inscrição Individual: Para jogadoras sem time. A organização formará equipes chamadas “Equipes Passa a Bola”.
    Documentos e Requisitos Obrigatórios
        Idade mínima: 18 anos até a data da inscrição.
        Cópia digitalizada de documento de identificação.
        Atestado médico de aptidão para prática de atividade física, emitido nos últimos 6 meses.
    Prazos e Taxas
    `;
    inputEventReward.value = `Premiação
        Equipe Campeã: Troféu, medalhas e prêmio de R$ 3.000,00.
        Vice-Campeã: Troféu, medalhas e prêmio de R$ 1.500,00.
        Destaques Individuais: Artilheira, Melhor Goleira e Craque do Campeonato.`
    inputMinAge.value = '18'
    inputMaxAge.value = '25'
    inputMaxTotalTeam.value = '20'
    inputMaxTotalUni.value = '200'
    inputCostUni.value = '30'
    inputCostTeam.value = '60'
    inputLinkedin.value = '@passabola'
    inputInstagram.value = '@passabola'
    inputOther.value = '@passabola'
}

const handleCleanFields = function() {
    title.value = ''
    mainTitle.innerText = title.value
    inputEventDateStart.value = ''
    inputDateEventEnd.value = ''
    inputAddressEvent.value = ''
    selectState.value = ''
    inputWhatsapp.value = ''
    inputEventDescription.value = ''
    inputEventReward.value = ''
    inputMinAge.value = ''
    inputMaxAge.value = ''
    inputMaxTotalTeam.value = ''
    inputMaxTotalUni.value = ''
    inputCostUni.value = ''
    inputCostTeam.value = ''
    inputLinkedin.value = ''
    inputInstagram.value = ''
    inputOther.value = ''
}

title.addEventListener('input', handlerInputOnChange);
title.addEventListener('change', handlerInputOnChange);
btnAuto.addEventListener('click', handlerDefaultInput);
btnClean.addEventListener('click', handleCleanFields);