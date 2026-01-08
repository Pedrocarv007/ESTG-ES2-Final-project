// Permite sair da seleção de pasta ao clicar fora
document.addEventListener('click', function(event) {
  // Se houver input de renomear aberto, cancela ao clicar fora
  document.querySelectorAll('input[type="text"]:not([style*="display: none"])').forEach(function(input) {
    if (!input.contains(event.target) && !input.parentElement.querySelector('.rename-folder-btn, .rename-material-btn')?.contains(event.target)) {
      input.blur();
    }
  });

  // Remover seleção visual de pastas/arquivos
  const explorer = document.querySelector('.explorer-table, .sidebar-folder');
  if (explorer && !explorer.contains(event.target)) {
    document.querySelectorAll('.selected').forEach(function(el) {
      el.classList.remove('selected');
    });
    // Ir para a raiz das pastas (explorer principal)
    // Supondo que a raiz é /materials/explorer_full
    window.location.href = 'https://www.thecarv.com/studyhubai/materials/explorer_full';
  }
});
// JS para renomear pastas e materiais inline

document.addEventListener('DOMContentLoaded', function () {
  // Renomear pasta (sidebar e subfolders)
  // Clique no lápis para renomear pasta
  document.querySelectorAll('.rename-folder-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const folderId = btn.getAttribute('data-folder-id');
      const link = btn.parentElement.querySelector('a');
      const oldName = link.textContent.replace('📁', '').trim();
      const input = document.createElement('input');
      input.type = 'text';
      input.value = oldName;
      input.style = 'width: 80%';
      link.style.display = 'none';
      btn.style.display = 'none';
      link.parentElement.insertBefore(input, link);
      input.focus();
      input.onblur = function() { restore(); };
      input.onkeydown = function(ev) {
        if (ev.key === 'Enter') {
          fetch(`/materials/folder/${folderId}/rename`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `name=${encodeURIComponent(input.value)}`
          }).then(r => r.json()).then(data => {
            if (data.success) {
              restore(data.name);
              location.reload();
            } else {
              alert(data.error || 'Erro ao renomear');
              restore();
            }
          });
        } else if (ev.key === 'Escape') {
          restore();
        }
      };
      function restore(newName) {
        link.textContent = '📁 ' + (newName || oldName);
        link.style.display = '';
        btn.style.display = '';
        input.remove();
      }
    });
  });

  // Renomear material (tabela)
  // Clique no lápis para renomear material
  document.querySelectorAll('.rename-material-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      const matId = btn.getAttribute('data-material-id');
      const link = btn.parentElement.querySelector('.name-link');
      const oldTitle = link.textContent.trim();
      const input = document.createElement('input');
      input.type = 'text';
      input.value = oldTitle;
      input.style = 'width: 80%';
      link.style.display = 'none';
      btn.style.display = 'none';
      link.parentElement.insertBefore(input, link);
      input.focus();
      input.onblur = function() { restore(); };
      input.onkeydown = function(ev) {
        if (ev.key === 'Enter') {
          fetch(`/materials/material/${matId}/rename`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `title=${encodeURIComponent(input.value)}`
          }).then(r => r.json()).then(data => {
            if (data.success) {
              restore(data.title);
              location.reload();
            } else {
              alert(data.error || 'Erro ao renomear');
              restore();
            }
          });
        } else if (ev.key === 'Escape') {
          restore();
        }
      };
      function restore(newTitle) {
        link.textContent = newTitle || oldTitle;
        link.style.display = '';
        btn.style.display = '';
        input.remove();
      }
    });
  });
});
