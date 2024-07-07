async function fetchLeaderboard() {
    const tableName = document.getElementById('tableName').value;
    const order = document.getElementById('order').value;
    const serverId = document.getElementById('serverId').value;
    const pageNumber = 1; // Start with the first page

    let url = `/leaderboard/${tableName}/${order}/${pageNumber}`;
    if (serverId) {
        url += `/${serverId}`;
    }

    const response = await fetch(url);
    const data = await response.json();
    const leaderboard = document.getElementById('leaderboard');
    leaderboard.innerHTML = '';

    data.forEach(user => {
        const li = document.createElement('li');
        li.textContent = `${user.username}: ${user[order]}`;
        leaderboard.appendChild(li);
    });
}
