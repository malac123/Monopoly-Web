// static/game.js

document.addEventListener('DOMContentLoaded', function() {
    const setupForm = document.getElementById('setup-form');
    if (setupForm) {
        setupForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const errorDiv = document.getElementById('setup-error');
            errorDiv.textContent = '';
            // Collect player names
            const playerInputs = document.querySelectorAll('input[name="player_names"]');
            const player_names = Array.from(playerInputs).map(input => input.value.trim()).filter(Boolean);
            if (player_names.length < 2 || player_names.length > 8) {
                errorDiv.textContent = 'Bitte 2-8 Spielernamen eingeben.';
                return;
            }
            // Call API
            try {
                const res = await fetch('/api/create_game', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ player_names })
                });
                const data = await res.json();
                if (res.status === 403 && data.redirect) {
                    window.location.href = data.redirect;
                    return;
                }
                if (res.ok && data.game_id) {
                    // Store game_id in sessionStorage and go to game page
                    sessionStorage.setItem('game_id', data.game_id);
                    window.location.href = '/game.html';
                } else {
                    errorDiv.textContent = data.error || 'Fehler beim Erstellen des Spiels.';
                }
            } catch (err) {
                errorDiv.textContent = 'Serverfehler.';
            }
        });
    }
}); 