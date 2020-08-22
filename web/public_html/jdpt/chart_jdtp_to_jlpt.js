<script>

var myChart = new Chart(document.getElementById(current_chart), {
    type: 'scatter',
    data: {
        labels: current_label,
        datasets: [{
                label: 'Distance',
                borderColor: 'black', // Add custom color border
                backgroundColor: '#2196f3', // Add custom color background (Points and Fill)
                data: current_data,
                pointRadius: 10,
                pointHoverRadius: 12
            }
        ]
    },
    options: {
        tooltips: {
            bodyFontSize: 20,
            callbacks: {
                label: function (tooltipItem, data) {
                    var value = data.labels[tooltipItem.index];
                    return value;
                }
            }
        },

        legend: {
            display: false
        },
        title: {
            display: true,
            text: current_title
        },
        scales: {
            yAxes: [{
                    type: 'logarithmic',
                    ticks: {
                        callback: function (tick, index, ticks) {
                            return tick.toLocaleString()
                        }
                    },
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Count',
                        fontSize: 16
                    }
                }
            ],
            xAxes: [{
                    type: 'linear',
                    position: 'bottom',
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Distance',
                        fontSize: 16
                    },
                    gridLines: {
                        display: true
                    },					
                    ticks: {
						stepSize : 1,
						max: 4.5
                    },
                }
            ]
        },
        plugins: {
            datalabels: {
                align: 'right',
                offset: 16,
                font: {
                    weight: 'bold'
                },

                formatter: function (value, context) {
                    return context.chart.data.labels[context.dataIndex];
                }

            }
        }
    }

});

</script>