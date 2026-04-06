# Projeto-01-Bitdoglab-v7

## Introdução: 
Esse é um projeto para a matéria EA801 turma V usando a Bitdoglab v7.

Nesse projeto, foi desenvolvido um jogo no estilo Guitar Hero, no qual aparecem notas de três cores diferentes nas colunas de uma matriz de LEDs. Para pontuar, o jogador deve pressionar o botão correspondente à coluna correta no momento exato em que a nota atinge a posição indicada.

O jogo possui um menu exibido em um display OLED SSD1306, que inclui um sistema de leaderboard, responsável por registrar as três melhores pontuações, além de um sistema de seleção de dificuldade.

Durante a partida, uma música no estilo 8-bit é reproduzida, variando de acordo com a dificuldade escolhida e também no menu, tornando a experiência mais dinâmica e imersiva.


Figura 1: Bitdoglab usada para o projeto
<img width="2880" height="2160" alt="image" src="https://github.com/user-attachments/assets/0a7a6356-0f36-42d0-933f-ed532c56dfe3" />

## Como usar? 
Para executar o projeto, basta rodar o script jogo_guitarhero.py em um ambiente de desenvolvimento compatível com MicroPython, como o Thonny.

Conecte a BitDogLab ao computador via USB, selecione a porta correta no compilador e execute o código. Certifique-se de que a biblioteca do display SSD1306 esteja previamente instalada na placa. Caso o arquivo não esteja presente, basta adicionar o arquivo ssd1306.py na BitDogLab. Esse arquivo pode ser encontrado neste repositório.

## Pinos usados: 
Foram utilizados os seguintes componentes e conexões:

Joystick: Eixo vertical → GP26/Eixo horizontal → GP27    
Matriz de LEDs: Conectada ao pino GP7           
Buzzer: Conectada ao GP21                       
Botões: Botão A → GP5 | Botão B → GP6 | Botão C → GP10    
Display OLED SSD1306 (I2C): SDA → GP2 | SCL → GP3








