/* Espera o conteúdo da página carregar */
document.addEventListener('DOMContentLoaded', () => {
    
    // Inicia a função da barra de scroll
    initializeCustomScrollbar();
    
    // Inicia a função das estrelas
    createStars();

    // Inicia a função do carrossel
    initializeCarousel();

    console.log('✨ StudyHub AI (Novo Design) Inicializado!');
});


/**
 * Função 1: Animação das Estrelas
 * (Este é o código que estava no seu base.html)
 */
function createStars() {
    const starsContainer = document.getElementById('stars-container');
    if (!starsContainer) return;

    starsContainer.innerHTML = ''; // Limpa estrelas antigas
    const numStars = 40;

    for (let i = 0; i < numStars; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        
        // Tamanhos aleatórios
        const sizes = ['small', 'medium', 'large'];
        const weights = [0.7, 0.25, 0.05];
        let randomSize = 'small';
        const rand = Math.random();
        
        if (rand < weights[2]) randomSize = 'large';
        else if (rand < weights[1] + weights[2]) randomSize = 'medium';
        
        star.classList.add(randomSize);
        star.style.left = Math.random() * 100 + '%';
        star.style.top = Math.random() * 100 + '%';
        star.style.animationDelay = Math.random() * 3 + 's';
        starsContainer.appendChild(star);
    }
    
    createShootingStars(starsContainer);

    // Recria estrelas cadentes periodicamente
    setInterval(() => {
        const shootingStars = starsContainer.querySelectorAll('.shooting-star');
        shootingStars.forEach(star => star.remove());
        createShootingStars(starsContainer);
    }, 30000); // A cada 30 segundos
}

function createShootingStars(starsContainer) {
    if (!starsContainer) return;
    const numShootingStars = 3;
    
    for (let i = 0; i < numShootingStars; i++) {
        const shootingStar = document.createElement('div');
        shootingStar.className = 'shooting-star';
        shootingStar.style.left = Math.random() * 100 + '%';
        shootingStar.style.top = Math.random() * 30 + '%';
        shootingStar.style.animationDelay = (Math.random() * 20 + 10) + 's';
        starsContainer.appendChild(shootingStar);
    }
}


/**
 * Função 2: Barra de Scroll Laranja Customizada
 * (Esta função liga a scrollbar falsa à scrollbar real)
 */
function initializeCustomScrollbar() {
    const mainContent = document.querySelector('main'); 
    const scrollThumb = document.querySelector('.custom-scrollbar-thumb');
    const scrollTrack = document.querySelector('.custom-scrollbar-track');

    if (!mainContent || !scrollThumb || !scrollTrack) {
        return; // Não executa se os elementos não existirem
    }

    function updateScrollbar() {
      mainContent.style.overflowY = "auto";
        const totalHeight = mainContent.scrollHeight;
        const visibleHeight = mainContent.clientHeight;

        // Esconde a barra se não houver scroll
        if (totalHeight <= visibleHeight) {
            scrollTrack.style.display = 'none';
            return;
        } else {
            scrollTrack.style.display = 'block';
        }

        // 1. Atualiza o tamanho do polegar
        const trackHeight = scrollTrack.clientHeight;
        const thumbHeight = (visibleHeight / totalHeight) * trackHeight;
        scrollThumb.style.height = `${Math.max(thumbHeight, 20)}px`; // Mínimo de 20px

        // 2. Atualiza a posição do polegar
        const scrollPosition = mainContent.scrollTop;
        const maxScroll = totalHeight - visibleHeight;
        const scrollPercentage = scrollPosition / maxScroll;
        const maxThumbPosition = trackHeight - scrollThumb.clientHeight;
        const thumbPosition = scrollPercentage * maxThumbPosition;

        scrollThumb.style.top = `${thumbPosition}px`;
    }

    // Ouve o evento de 'scroll' no <main>
    mainContent.addEventListener('scroll', updateScrollbar);
    
    // Ouve mudanças no tamanho (ex: se o browser mudar de tamanho)
    const resizeObserver = new ResizeObserver(updateScrollbar);
    resizeObserver.observe(mainContent);

    // Chama a função uma vez no início para acertar a posição
    updateScrollbar();
}
/**
 * Função 3: Carrossel de Grupos
 * (Esta função controla as setas e as classes 'active-card')
 */
function initializeCarousel() {
  const track = document.querySelector(".carousel-track");
  const leftArrow = document.querySelector(".left-arrow");
  const rightArrow = document.querySelector(".right-arrow");

  // Verifica se estamos na página que tem o carrossel
  if (!track || !leftArrow || !rightArrow) {
    return;
  }

  // Obter todos os cartões como uma lista
  const cards = Array.from(track.children);
  
  // Encontrar o índice do cartão que está ativo
  let currentIndex = cards.findIndex(card => 
    card.classList.contains("active-card")
  );

  // Função para atualizar as classes
  function updateCarousel(newIndex) {
    // Limita o índice para não sair dos limites da lista
    if (newIndex < 0) {
        newIndex = 0; // Ou newIndex = cards.length - 1; para dar a volta
    } else if (newIndex >= cards.length) {
        newIndex = cards.length - 1; // Ou newIndex = 0; para dar a volta
    }

    // Remove as classes de todos
    cards.forEach(card => {
      card.classList.remove("active-card");
      card.classList.remove("side-card");
    });

    // Adiciona a classe ativa ao cartão do centro
    cards[newIndex].classList.add("active-card");

    // Adiciona a classe lateral aos vizinhos (se existirem)
    if (cards[newIndex - 1]) {
      cards[newIndex - 1].classList.add("side-card");
    }
    if (cards[newIndex + 1]) {
      cards[newIndex + 1].classList.add("side-card");
    }
    
    // Atualiza o índice atual
    currentIndex = newIndex;
  }

  // Ouve os cliques nas setas
  leftArrow.addEventListener("click", () => {
    updateCarousel(currentIndex - 1);
  });

  rightArrow.addEventListener("click", () => {
    updateCarousel(currentIndex + 1);
  });
  
  // Inicia o carrossel na posição correta (caso o HTML não esteja certo)
  updateCarousel(currentIndex);
}