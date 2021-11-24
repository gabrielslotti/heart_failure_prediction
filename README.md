<h1 align="center">
    <a>Predição de doenças cardiovasculares</a>
</h1>
<p align="center">Modelo elaborado para predição de falhas cardíacas e doenças cardiovasculares.</p>

<h3>Índice</h3>
<p align="left">
 • <a href="#business-ctx">Contexto de negócio</a></br>
 • <a href="#dataset-desc">Dataset</a></br>
 • <a href="#attr-desc">Descrição dos atributos do dataset</a></br>
 • <a href="#pre-process">Pré-processamento das variáveis</a></br>
 • <a href="#models">Modelos</a></br>
 • <a href="#results">Avaliação de desempenho</a></br>
 • <a href="#refs">Distribuição</a></br>
 • <a href="#refs">Referências</a>
</p>

<h3 id="business-ctx">Contexto de negócio</h3>
<p>"As doenças cardiovasculares são a principal causa de morte no mundo: mais pessoas morrem anualmente por essas enfermidades do que por qualquer outra causa.

Estima-se que 17,9 milhões de pessoas morreram por doenças cardiovasculares em 2016, representando 31% de todas as mortes em nível global. Destes óbitos, estima-se que 85% ocorrem devido a ataques cardíacos e acidentes vasculares cerebrais (AVCs).

Mais de três quartos das mortes por doenças cardiovasculares ocorrem em países de baixa e média renda.

Das 17 milhões de mortes prematuras (pessoas com menos de 70 anos) por doenças crônicas não transmissíveis, 82% acontecem em países de baixa e média renda e 37% são causadas por doenças cardiovasculares" (OPAS/OMS).</p>

<h3 id="dataset-desc">Dataset</h3>
<p>Para a construção do modelo, foi utilizado o seguinte dataset disponível no Kaggle: <a href="https://www.kaggle.com/fedesoriano/heart-failure-prediction">Heart Failure Prediction Dataset</a>.</p>

<h3 id="attr-desc">Descrição dos atributos do dataset</h3>
<table border="1">
    <tr>
        <td>Atributo</td>
        <td>Tipo</td>
        <td>Descrição</td>
    </tr>
    <tr>
        <td>Age</td>
        <td>Numérico</td>
        <td>Idade do paciente em anos.</td>
    </tr>
    <tr>
        <td>Sex</td>
        <td>Binário</td>
        <td>Sexo do paciente [M: Male, F: Female].</td>
    </tr>
    <tr>
        <td>ChestPainType</td>
        <td>Nominal</td>
        <td>Tipo de dor no peito [TA: Typical Angina, ATA: Atypical Angina, NAP: Non-Anginal Pain, ASY: Asymptomatic].</td>
    </tr>
    <tr>
        <td>RestingBP</td>
        <td>Numérico</td>
        <td>Pressão sanguínea em repouso em mmHg (milímetro de mercúrio).</td>
    </tr>
    <tr>
        <td>Cholesterol</td>
        <td>Numérico</td>
        <td>Colesterol em mm/dL (milímetro por decilitro).</td>
    </tr>
    <tr>
        <td>FastingBS</td>
        <td>Binário</td>
        <td>Açucar no sanguem em jejum, 1 se FastingBS > 120 mg/dL senão 0.</td>
    </tr>
    <tr>
        <td>RestingECG</td>
        <td>Nominal</td>
        <td>Resultados de eletrocardiograma em repouso [Normal: Normal, ST: having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV), LVH: showing probable or definite left ventricular hypertrophy by Estes' criteria].</td>
    </tr>
    <tr>
        <td>MaxHR</td>
        <td>Numérico</td>
        <td>Frequência cardíaca máxima alcançada, valor numérico entre 60 e 202.</td>
    </tr>
    <tr>
        <td>ExerciseAngina</td>
        <td>Binário</td>
        <td>Angina induzida por exercício [Y: Yes, N: No].</td>
    </tr>
    <tr>
        <td>Oldpeak</td>
        <td>Numérico</td>
        <td>Depressão do segmento ST induzida por exercício em relação ao descanso.</td>
    </tr>
    <tr>
        <td>ST_Slope</td>
        <td>Binário</td>
        <td>Inclinação do pico em exercício do segmento ST [Up: upsloping, Flat: flat, Down: downsloping].</td>
    </tr>
    <tr>
        <td>HeartDisease</td>
        <td>Binário</td>
        <td>Indica se o paciente possuí doença cardíaca [1: heart disease, 0: Normal].</td>
    </tr>
</table>

<h3 id="pre-process">Pré-processamento das variáveis</h3>
<table border="1">
    <tr>
        <td>Variável</td>
        <td>Descrição</td>
    </tr>
    <tr>
        <td>PRE_AGE</td>
        <td>Se "Age" >= 50 então 1 senão normalização linear (max = 50, min = 28).</td>
    </tr>
    <tr>
        <td>PRE_SEX_M</td>
        <td>Se "Sex" igual a "M" então 1 senão 0.</td>
    </tr>
    <tr>
        <td>PRE_SEX_F</td>
        <td>Se "Sex" igual a "F" então 1 senão 0.</td>
    </tr>
    <tr>
        <td>PRE_CHEST_PAIN_TYPE_NAP</td>
        <td>Se "ChestPainType" = "NAP" então 1 senão 0.</td>
    </tr>
    <tr>
        <td>PRE_CHEST_PAIN_TYPE_ATA</td>
        <td>Se "ChestPainType" = "ATA" então 1 senão 0.</td>
    </tr>
    <tr>
        <td>PRE_CHEST_PAIN_TYPE_ASY</td>
        <td>Se "ChestPainType" = "ASY" então 1 senão 0.</td>
    </tr>
    <tr>
        <td>PRE_CHEST_PAIN_TYPE_TA</td>
        <td>Se "ChestPainType" = "TA" então 1 senão 0.</td>
    </tr>
    <tr>
        <td>PRE_RESTING_BP</td>
        <td>Se "RestingBP" > 139 então 1 senão normalização linear (max = 139, min = 80).</td>
    </tr>   
    <tr>
        <td>PRE_CHOLESTEROL_CAT</td>
        <td>Se "Cholesterol" > 239 então 1 senão 0.</td>
    </tr>  
    <tr>
        <td>PRE_CHOLESTEROL</td>
        <td>Se "Cholesterol" > 239 então 1 senão normalização linear (max = 239, min = 85).</td>
    </tr>
    <tr>
        <td>PRE_FASTING_BP</td>
        <td>Valor da coluna "FastingBP" (1 se FastingBS > 120 mg/dL senão 0).</td>
    </tr>
    <tr>
        <td>PRE_RESTING_ECG</td>
        <td>Se "RestingECG" <> "Normal" entçao 0 senão 1.</td>
    </tr>
    <tr>
        <td>PRE_MAX_HR_CAT</td>
        <td>Se "MaxHR" > 128 então 1 senão 0.</td>
    </tr>
    <tr>
        <td>PRE_MAX_HR</td>
        <td>Se "MaxHR" > 128 então 1 senão normalização linear (max = 128, min = 60).</td>
    </tr>
    <tr>
        <td>PRE_EXERCISE_ANGINA</td>
        <td>Se "ExerciseAngina" = 'Y' então 1 senão 0.</td>
    </tr>
    <tr>
        <td>PRE_OLDPEAK</td>
        <td>Normalização linear (max = 6.2, min = -2).</td>
    </tr>
    <tr>
        <td>PRE_ST_SLOPE</td>
        <td>Se "Oldpeak" <> 'Flat' então 1 senão 0.</td>
    </tr>
</table>

<h3 id="models">Modelos</h3>
<p>Para um melhor entendimento de qual seria o melhor algoritmo para elaboração do modelo, foram testado alguns algoritmos: Naive-Bayes, Decision Tree, RNA, Extra Trees, Baggin com Naive-Bayes e Bagging com Decision Tree.</p>
<p>Todos os algoritmos utilizaram as mesmas variáveis pré-processadas.</p>

<h3 id="results">Avaliação de desempenho</h3>
<p></p>

<h3 id="impl">Distribuição</h3>
<p></p>

<h3 id="refs">Referências</h3>
<p>1. fedesoriano. (September 2021). Heart Failure Prediction Dataset. Disponível em: https://www.kaggle.com/fedesoriano/heart-failure-prediction. Acesso em: 21 de out. de 2021.</p>
<p>2. Organização Pan-Americana da Saúde. Disponível em: https://www.paho.org/pt/topicos/doencas-cardiovasculares. Acesso em: 23 de nov. de 2021.</p>
