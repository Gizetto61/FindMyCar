function changeMainImage(element) {
    const mainImage = document.getElementById('mainImage');
    const src = element.src || element.getAttribute('src');
    
    // Remover classe active de todas as miniaturas
    document.querySelectorAll('.thumbnail-active').forEach(el => {
        el.classList.remove('thumbnail-active');
    });
    
    // Adicionar classe active à miniatura clicada
    element.classList.add('thumbnail-active');
    
    // Trocar imagem com efeito fade
    mainImage.style.opacity = '0';
    
    setTimeout(() => {
        mainImage.src = src;
        mainImage.style.opacity = '1';
    }, 200);
}


// Função para compartilhar
function shareVehicle() {
    if (navigator.share) {
        navigator.share({
            title: document.title,
            text: 'Confira este carro incrível!',
            url: window.location.href
        }).catch(err => console.log('Erro ao compartilhar:', err));
    } else {
        navigator.clipboard.writeText(window.location.href);
        alert('Link copiado para a área de transferência!');
    }
}

// Função para falar com o vendedor
function contactSeller(phone) {
    // Remove caracteres não numéricos e adiciona código do país se necessário
    const cleanPhone = phone.replace(/\D/g, '');
    const fullPhone = cleanPhone.startsWith('55') ? cleanPhone : '55' + cleanPhone;
    window.open(`https://wa.me/${fullPhone}`, '_blank');
}

// Inicialização quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    
    // Marcar a primeira miniatura como ativa
    const firstThumbnail = document.querySelector('.grid img[onclick]');
    if (firstThumbnail) {
        firstThumbnail.classList.add('thumbnail-active');
    }
    
    // Animação suave das barras de progresso
    const progressBars = document.querySelectorAll('[class*="bg-indigo-600 h-2"]');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
    
    // Smooth scroll para links âncora
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Carrossel de imagens (navegação com teclado)
document.addEventListener('keydown', function(e) {
    const thumbnails = Array.from(document.querySelectorAll('.grid img[onclick]'));
    const currentActive = document.querySelector('.thumbnail-active');
    
    if (!currentActive || thumbnails.length === 0) return;
    
    const currentIndex = thumbnails.indexOf(currentActive);
    
    if (e.key === 'ArrowRight' && currentIndex < thumbnails.length - 1) {
        const nextThumbnail = thumbnails[currentIndex + 1];
        changeMainImage(nextThumbnail);
    } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
        const prevThumbnail = thumbnails[currentIndex - 1];
        changeMainImage(prevThumbnail);
    }
});
