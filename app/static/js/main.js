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
    if (!starsContainer) {
        console.error('❌ Container de estrelas não encontrado!');
        return;
    }

    console.log('🌟 Iniciando criação das estrelas...');
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
    
    // Cria as estrelas cadentes iniciais
    createShootingStars(starsContainer);
    
    console.log('✨ Estrelas normais criadas:', starsContainer.querySelectorAll('.star').length);
    console.log('🌠 Estrelas cadentes criadas:', starsContainer.querySelectorAll('.shooting-star').length);

    // Recria estrelas cadentes periodicamente
    setInterval(() => {
        const shootingStars = starsContainer.querySelectorAll('.shooting-star');
        shootingStars.forEach(star => star.remove());
        createShootingStars(starsContainer);
        console.log('🔄 Estrelas cadentes recriadas');
    }, 15000); // A cada 15 segundos (mais frequente)
}



function createShootingStars(starsContainer) {
    if (!starsContainer) {
        console.error('❌ Container não fornecido para estrelas cadentes!');
        return;
    }
    
    console.log('🌠 Criando estrelas cadentes...');
    const numShootingStars = 3;
    
    for (let i = 0; i < numShootingStars; i++) {
        const shootingStar = document.createElement('div');
        shootingStar.className = 'shooting-star';
        
        // Posição aleatória na parte superior da tela
        const leftPos = Math.random() * 100;
        const topPos = Math.random() * 30;
        
        shootingStar.style.left = leftPos + '%';
        shootingStar.style.top = topPos + '%';
        
        // Delay aleatório para que não apareçam todas ao mesmo tempo
        const randomDelay = Math.random() * 5; // Reduzindo o delay para debug
        shootingStar.style.animationDelay = randomDelay + 's';
        
        // Duração aleatória da animação
        const randomDuration = (Math.random() * 3 + 6); // Entre 6-9 segundos
        shootingStar.style.animationDuration = randomDuration + 's';
        
        // Adiciona atributos de debug
        shootingStar.setAttribute('data-debug', `star-${i}`);
        shootingStar.style.setProperty('--debug-left', leftPos + '%');
        shootingStar.style.setProperty('--debug-top', topPos + '%');
        
        starsContainer.appendChild(shootingStar);
        
        console.log(`🌠 Estrela cadente ${i + 1}:`, {
            left: leftPos + '%',
            top: topPos + '%',
            delay: randomDelay + 's',
            duration: randomDuration + 's'
        });
    }
    
    // Verificar se as estrelas foram realmente adicionadas
    const addedStars = starsContainer.querySelectorAll('.shooting-star');
    console.log(`✅ Total de estrelas cadentes no DOM: ${addedStars.length}`);
}

// Função para testar estrelas cadentes manualmente (use no console do navegador)
function testShootingStars() {
    const starsContainer = document.getElementById('stars-container');
    if (starsContainer) {
        // Remove estrelas cadentes existentes
        const existing = starsContainer.querySelectorAll('.shooting-star');
        existing.forEach(star => star.remove());
        
        // Cria novas com delay mínimo para teste
        createTestShootingStars(starsContainer);
        console.log('🧪 Teste de estrelas cadentes executado!');
    }
}

// Função para criar estrelas cadentes de teste (sem delay)
function createTestShootingStars(starsContainer) {
    for (let i = 0; i < 2; i++) {
        const shootingStar = document.createElement('div');
        shootingStar.className = 'shooting-star';
        
        shootingStar.style.left = (20 + i * 30) + '%';
        shootingStar.style.top = '10%';
        shootingStar.style.animationDelay = '0s'; // Sem delay
        shootingStar.style.animationDuration = '5s';
        
        starsContainer.appendChild(shootingStar);
        console.log(`🧪 Estrela de teste ${i + 1} criada`);
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

  // Encontrar o índice do cartão que está ativo, se não houver, começa do meio
  let currentIndex = cards.findIndex(card => card.classList.contains("active-card"));
  if (currentIndex === -1) {
    currentIndex = Math.floor(cards.length / 2);
  }

  // Função para atualizar as classes
  function updateCarousel(newIndex) {
    // Torna o carrossel circular
    if (newIndex < 0) {
      newIndex = cards.length - 1;
    } else if (newIndex >= cards.length) {
      newIndex = 0;
    }

    // Remove as classes de todos
    cards.forEach(card => {
      card.classList.remove("active-card", "side-card");
    });

    // Adiciona a classe ativa ao cartão do centro
    cards[newIndex].classList.add("active-card");

    // Adiciona a classe lateral aos vizinhos (se existirem)
    const leftIdx = (newIndex - 1 + cards.length) % cards.length;
    const rightIdx = (newIndex + 1) % cards.length;
    if (cards.length > 1) cards[leftIdx].classList.add("side-card");
    if (cards.length > 2) cards[rightIdx].classList.add("side-card");

    // Debug: log do estado atual
    console.log("Carrossel:", cards.map((c, i) => ({
      idx: i,
      active: c.classList.contains("active-card"),
      side: c.classList.contains("side-card")
    })));

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

// Dropdown de usuário: fecha ao clicar fora
(function() {
  document.addEventListener('click', function(e) {
    const dropdown = document.querySelector('.user-dropdown');
    if (!dropdown) return;
    const menu = dropdown.querySelector('.user-dropdown-menu');
    if (!menu) return;
    if (!dropdown.contains(e.target)) {
      menu.style.display = 'none';
    } else {
      menu.style.display = 'block';
    }
  });
})();