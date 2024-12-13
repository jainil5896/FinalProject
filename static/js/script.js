document.getElementById('paymentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());
    console.log(data);
    fetch('/api/payments', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        console.log('Response status:', response.status); // Log the response status
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data); // Log the response data
        loadPayments(); // Refresh the payment table
    })
    .catch(error => console.error('Error:', error));
});

function loadPayments() {
    fetch('/api/payments')
    .then(response => response.json())
    .then(data => {
        const tableDiv = document.getElementById('paymentTable');
        tableDiv.innerHTML = ''; // Clear existing table
        const table = document.createElement('table');
        table.innerHTML = `
            <tr>
                <th>ID</th>
                <th>Company</th>
                <th>Amount</th>
                <th>Payment Date</th>
                <th>Status</th>
                <th>Due Date</th>
            </tr>
        `;
        data.forEach(payment => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${payment.id}</td>
                <td>${payment.company}</td>
                <td>${payment.amount}</td>
                <td>${payment.payment_date}</td>
                <td>${payment.status}</td>
                <td>${payment.due_date}</td>
            `;
            table.appendChild(row);
        });
        tableDiv.appendChild(table);
    });
}

// Load payments on page load
document.addEventListener('DOMContentLoaded', loadPayments);