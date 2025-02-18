document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById('trendsChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            datasets: [{
                label: 'Sales Trends',
                data: [500, 750, 620, 880, 900, 1100, 1200],
                borderColor: '#A28F70',
                backgroundColor: 'rgba(162, 143, 112, 0.2)',
                borderWidth: 3,
                pointRadius: 5,
                pointBackgroundColor: '#8B6E4E',
                tension: 0 // Set to 0 to make the lines sharp
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
// function toggleSidebar() {
//     const sidebar = document.getElementById('sidebar');
//     const mainContent = document.getElementById('main-content');
//     sidebar.classList.toggle('collapsed');
//     mainContent.classList.toggle('expanded');
// }
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
    
    // Save the state to localStorage
    const isCollapsed = sidebar.classList.contains('collapsed');
    localStorage.setItem('sidebarCollapsed', isCollapsed);
}

// Restore sidebar state on page load
window.addEventListener('load', () => {
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (isCollapsed) {
        document.getElementById('sidebar').classList.add('expanded');
        document.getElementById('mainContent').classList.add('collapsed');   
    }
});

function activateTab(tab) {
    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    // Add active class to clicked tab
    tab.classList.add('active');
}

// Add click event listeners to all tabs
document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', (e) => {
        e.preventDefault();
        activateTab(tab);
    });
});

let chartInstance = null;

function showGraph(index) {
    document.getElementById('overlay').style.display = 'flex';

    const ctx = document.getElementById('zoomChart').getContext('2d');

    if (chartInstance) {
        chartInstance.destroy(); // Clear previous chart before rendering a new one
    }

    const hourlyLabels = [
        "12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM",
        "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"
    ];

    const dailyLabels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

    const weeklyLabels = ["Week 1", "Week 2", "Week 3", "Week 4"];

    const monthlyLabels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun", 
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ];

    const dataSets = [
        { 
            label: "Hourly Sales", 
            data: [5, 8, 12, 15, 20, 18, 22, 35, 50, 60, 75, 80, 85, 90, 95, 100, 105, 110, 90, 80, 70, 60, 50, 40],
            type: 'bar',
            labels: hourlyLabels,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)'
            ],
            borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)'
            ],
        },
        {
        label: "Daily Sales",
        data: [
            { x: 1, y: 500 }, { x: 2, y: 700 }, { x: 3, y: 850 }, { x: 4, y: 920 }, { x: 5, y: 1020 }, { x: 6, y: 1070 }, { x: 7, y: 1150 }
        ],
        type: 'scatter',
        labels: dailyLabels,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgb(75, 192, 192)',
        pointBackgroundColor: 'rgb(75, 192, 192)',
        pointBorderColor: 'rgb(75, 192, 192)',
        pointRadius: 6
    },
        { 
            label: "Weekly Sales", 
            data: [1350, 1500, 2000, 3500],
            type: 'line',
            labels: weeklyLabels,
            borderColor: 'rgb(162, 143, 112)',
            backgroundColor: 'rgba(162, 143, 112, 0.5)',
            pointBackgroundColor: 'rgb(162, 143, 112)',
            pointBorderColor: 'rgb(162, 143, 112)',
            pointRadius: 5,
            borderWidth: 3,
            fill: true
        },
        { 
            label: "Monthly Sales", 
            data: [4200, 4800, 5100, 5300, 6000, 6700, 7000, 7500, 7800, 8100, 8600, 9000], 
            type: 'pie',
            labels: monthlyLabels,
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',  // Jan
                'rgba(54, 162, 235, 0.5)',  // Feb
                'rgba(255, 205, 86, 0.5)',  // Mar
                'rgba(75, 192, 192, 0.5)',  // Apr
                'rgba(153, 102, 255, 0.5)', // May
                'rgba(255, 159, 64, 0.5)',  // Jun
                'rgba(201, 203, 207, 0.5)', // Jul
                'rgba(99, 255, 132, 0.5)',  // Aug
                'rgba(199, 21, 133, 0.5)',  // Sep
                'rgba(144, 238, 144, 0.5)', // Oct
                'rgba(0, 206, 209, 0.5)',   // Nov
                'rgba(128, 0, 128, 0.5)'    // Dec
            ],
            borderColor: '#fff'
        }
    ];

    const selectedDataset = dataSets[index];

    chartInstance = new Chart(ctx, {
        type: selectedDataset.type, // Set chart type dynamically
        data: {
            labels: selectedDataset.labels,
            datasets: [{
                label: selectedDataset.label,
                data: selectedDataset.data,
                backgroundColor: selectedDataset.backgroundColor,
                borderColor: selectedDataset.borderColor,
                pointBackgroundColor: selectedDataset.pointBackgroundColor,
                pointBorderColor: selectedDataset.pointBorderColor,
                borderWidth: 2,
                fill: index === 2 // Only fill for line chart
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: index !== 3, // Allows us to set custom size
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });

    // Resize the canvas for the pie chart to make it smaller
    if (index === 3) { // If it's the pie chart
        document.getElementById('zoomChart').style.width = "300px";
        document.getElementById('zoomChart').style.height = "500px";
    } else {
        document.getElementById('zoomChart').style.width = "auto";
        document.getElementById('zoomChart').style.height = "auto";
    }
}

function closeGraph() {
    document.getElementById('overlay').style.display = 'none';
}