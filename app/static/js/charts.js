document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('categoryChart');
    if (!canvas) return; // Only run this on pages that actually have the chart

    fetch('/api/summary')
        .then(response => response.json())
        .then(data => {
            // Aggregate total spend per category on the client side
            const categoryTotals = {};
            data.expenses.forEach(exp => {
                const cat = exp.category || 'Uncategorized';
                categoryTotals[cat] = (categoryTotals[cat] || 0) + exp.amount;
            });

            const labels = Object.keys(categoryTotals);
            const values = Object.values(categoryTotals);

            if (labels.length === 0) {
                canvas.replaceWith(document.createTextNode('Add some expenses to see your spending breakdown.'));
                return;
            }

            new Chart(canvas, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: values,
                        backgroundColor: [
                            '#6366f1', '#22c55e', '#f59e0b', '#ef4444',
                            '#06b6d4', '#8b5cf6', '#ec4899', '#84cc16'
                        ],
                        borderWidth: 2,
                        borderColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right'
                        }
                    }
                }
            });
        })
        .catch(err => console.error('Failed to load chart data:', err));
});