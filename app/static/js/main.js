/* Espera o conteúdo da página carregar */
document.addEventListener("DOMContentLoaded", () => {
  console.log("✨ StudyHub AI: Iniciando scripts...");

  // 1. Iniciar Scrollbar
  initializeCustomScrollbar();

  // 2. Iniciar Estrelas
  createStars();

  // 3. Iniciar Carrossel (apenas se existir na página)
  if (document.querySelector(".carousel-track")) {
    initializeCarousel();
  }
});

/* ==========================================
   FUNÇÃO 1: BARRA DE SCROLL CUSTOMIZADA (ROBUSTA)
   ========================================== */
function initializeCustomScrollbar() {
  const mainContent = document.querySelector("main");
  const scrollThumb = document.querySelector(".custom-scrollbar-thumb");
  const scrollTrack = document.querySelector(".custom-scrollbar-track");

  if (!mainContent || !scrollThumb || !scrollTrack) {
    console.warn("⚠️ Elementos da scrollbar não encontrados.");
    return;
  }

  function updateScrollbar() {
    const totalHeight = mainContent.scrollHeight;
    const visibleHeight = mainContent.clientHeight;
    const scrollPosition = mainContent.scrollTop;

  
     if (totalHeight <= visibleHeight + 1) {
      scrollTrack.style.display = "none";
      return;
    } else {
      scrollTrack.style.display = "block";
    }

    // 1. Calcular altura do polegar (Thumb)
    const trackHeight = scrollTrack.clientHeight;
    // Relação entre o que vemos e o total
    const ratio = visibleHeight / totalHeight;
    // Altura proporcional
    let thumbHeight = ratio * trackHeight;
    // Define um tamanho mínimo (20px) para não desaparecer
    thumbHeight = Math.max(thumbHeight, 30);
    
    scrollThumb.style.height = `${thumbHeight}px`;

    // 2. Calcular posição do polegar (Top)
    // Espaço disponível para o polegar se mover
    const maxThumbMove = trackHeight - thumbHeight;
    // Espaço disponível para rolar o conteúdo
    const maxScrollContent = totalHeight - visibleHeight;
    
    // Percentagem atual do scroll
    const scrollPercentage = scrollPosition / maxScrollContent;
    
    // Posição final
    const thumbTop = scrollPercentage * maxThumbMove;

    scrollThumb.style.top = `${thumbTop}px`;
  }

  // --- EVENT LISTENERS ---

  // 1. Quando o utilizador rola
  mainContent.addEventListener("scroll", updateScrollbar);

  // 2. Quando a janela muda de tamanho
  window.addEventListener("resize", updateScrollbar);

  // 3. Quando as imagens terminam de carregar (Importante!)
  window.addEventListener("load", updateScrollbar);

  // 4. Verificação periódica (segurança para conteúdo dinâmico)
  setInterval(updateScrollbar, 1000);

  // Chamada inicial
  updateScrollbar();
}

/* ==========================================
   FUNÇÃO 2: ESTRELAS ANIMADAS
   ========================================== */
function createStars() {
  const starsContainer = document.getElementById("stars-container");
  if (!starsContainer) return;

  starsContainer.innerHTML = "";
  const numStars = 50; // Reduzi um pouco para performance

  for (let i = 0; i < numStars; i++) {
    const star = document.createElement("div");
    star.className = "star";
    
    // Tamanho aleatório
    const r = Math.random();
    if (r < 0.7) star.classList.add("small");
    else if (r < 0.9) star.classList.add("medium");
    else star.classList.add("large");

    star.style.left = Math.random() * 100 + "%";
    star.style.top = Math.random() * 100 + "%";
    star.style.animationDelay = Math.random() * 3 + "s";
    starsContainer.appendChild(star);
  }
}

/* ==========================================
   FUNÇÃO 3: CARROSSEL INFINITO
   ========================================== */
function initializeCarousel() {
  const track = document.querySelector(".carousel-track");
  const leftArrow = document.querySelector(".left-arrow");
  const rightArrow = document.querySelector(".right-arrow");

  if (!track || !leftArrow || !rightArrow) return;

  const cards = Array.from(track.children);
  if (cards.length === 0) return;

  let currentIndex = cards.findIndex(c => c.classList.contains("active-card"));
  if (currentIndex === -1) currentIndex = 0;

  function updateCarousel() {
    // Resetar estilos
    cards.forEach(card => {
      card.className = "group-card"; // Remove active/side
      card.style.display = "none";
      card.style.order = "0";
    });

    // Calcular índices (Circular)
    const prev = (currentIndex - 1 + cards.length) % cards.length;
    const next = (currentIndex + 1) % cards.length;

    // Configurar Cartão Anterior
    cards[prev].style.display = "flex"; // "flex" para manter o CSS que corrigimos
    cards[prev].classList.add("side-card");
    cards[prev].style.order = "1";

    // Configurar Cartão Ativo
    cards[currentIndex].style.display = "flex";
    cards[currentIndex].classList.add("active-card");
    cards[currentIndex].style.order = "2";

    // Configurar Cartão Próximo
    cards[next].style.display = "flex";
    cards[next].classList.add("side-card");
    cards[next].style.order = "3";
  }

  leftArrow.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + cards.length) % cards.length;
    updateCarousel();
  });

  rightArrow.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % cards.length;
    updateCarousel();
  });

  // Inicializar
  updateCarousel();
}


/* ==========================================
   FUNÇÃO 4: Possibilitar ver a palavra-passe
   ========================================== */

   /**

 * Função para mostrar/esconder a senha
 * @param {string} inputId - O ID do campo de input
 * @param {HTMLElement} btn - O botão que foi clicado
 */
function togglePassword(inputId, btn) {
    const input = document.getElementById(inputId);
    const icon = btn.querySelector('svg');
    
    if (input.type === "password") {
        // Mostrar Senha
        input.type = "text";
        
        // Mudar Ícone para Olho Aberto
        icon.innerHTML = `
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
            <circle cx="12" cy="12" r="3"></circle>
        `;
        btn.style.color = "var(--color-main-purple)"; // Destaque visual
    } else {
        // Esconder Senha
        input.type = "password";
        
        // Mudar Ícone para Olho Fechado (Riscado)
        icon.innerHTML = `
            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
            <line x1="1" y1="1" x2="23" y2="23"></line>
        `;
        btn.style.color = "#999"; // Cor normal
    }
}