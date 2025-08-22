===========================
🧬 CLONE GAME - PYGAME
===========================

Clone Game é um mini game feito com Python e Pygame onde o jogador precisa sobreviver o máximo de tempo possível enquanto clones perseguem seus passos anteriores. Cada movimento pode se tornar uma armadilha futura — pense rápido, mova com estratégia e vença a si mesmo!

---------------------------
🎮 COMO JOGAR
---------------------------

- Use as setas do teclado para mover o jogador.
- A cada poucos segundos, clones surgem e seguem exatamente o caminho que você percorreu.
- Evite colidir com os clones — o jogo termina se você encostar em um deles.
- A arena vai ficando menor e os clones aparecem mais rápido conforme o nível aumenta.
- Pressione ENTER na tela inicial para começar e R na tela de Game Over para reiniciar.

---------------------------
🧠 MECÂNICAS
---------------------------

- Clones seguem o histórico de movimento do jogador com atraso.
- A dificuldade aumenta com o tempo: mais clones, arena menor, jogador mais rápido.
- Ranking com os 3 melhores tempos é salvo em "ranking.txt".
- Sons de clone e game over são gerados dinamicamente com numpy e wave.

---------------------------
📦 REQUISITOS
---------------------------

- Python 3.7 ou superior
- Pygame
- NumPy

Instale as dependências com:

pip install pygame numpy

---------------------------
🚀 EXECUTANDO O JOGO
---------------------------

1. Clone ou baixe o repositório.
2. Execute o arquivo principal:

   python clone_game.py

---------------------------
📁 ESTRUTURA DO PROJETO
---------------------------

clone_game/
├── clone_game.py         -> Código principal do jogo
├── clone.wav             -> Som de clone (gerado automaticamente)
├── gameover.wav          -> Som de game over (gerado automaticamente)
├── ranking.txt           -> Ranking dos melhores tempos

---------------------------
🏆 RANKING
---------------------------

Os 3 melhores tempos são salvos automaticamente após cada partida.
O ranking aparece na tela de Game Over.

---------------------------
✨ IDEIAS FUTURAS
---------------------------

- Power-ups (dash, escudo temporário, etc.)
- Modo multiplayer local
- Editor de níveis
- Animações e efeitos visuais
- Sistema de conquistas

---------------------------
📜 LICENÇA
---------------------------

Este projeto é de uso livre para fins educacionais e pessoais.
Sinta-se à vontade para modificar e compartilhar!

---------------------------
Feito com 💻 por Felipe
---------------------------
