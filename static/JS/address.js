async function fetchAddresses() {
    const token = localStorage.getItem('token');  // O donde estés guardando el JWT
    const response = await fetch('/addresses/<address_id>', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });

    if (response.ok) {
        const addresses = await response.json();
        displayAddresses(addresses);
    } else {
        console.error('Error fetching addresses:', response.status);
    }
}
