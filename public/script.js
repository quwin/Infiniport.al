async function fetchLeaderboard() {
    const tableName = document.getElementById('tableName').value;
    const order = document.getElementById('order').value;
    const guildHandle = document.getElementById('guildhandle').value.toLowerCase();
    const pageNumber = 1; // Start with the first page

    let url = `/leaderboard/${tableName}/${order}/${pageNumber}`;
    if (guildHandle) {
        url += `/${guildHandle}`;
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
