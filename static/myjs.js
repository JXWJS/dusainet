//book_list.html 渲染echiarts
function book_list(books_count) {
    // echarts
    for (var i = 0; i < books_count; i++) {
        // 基于准备好的dom，初始化echarts实例
        var myChart = echarts.init(document.getElementById('echarts_book_' + (i + 1)));
        var practicality = document.getElementById('practicality_' + (i + 1)).firstChild.nodeValue;
        var interesting = document.getElementById('interesting_' + (i + 1)).firstChild.nodeValue;
        var readability = document.getElementById('readability_' + (i + 1)).firstChild.nodeValue;
        var professionalism = document.getElementById('professionalism_' + (i + 1)).firstChild.nodeValue;
        var binding_quality = document.getElementById('binding_quality_' + (i + 1)).firstChild.nodeValue;
        // 指定图表的配置项和数据
        option = {
            tooltip: {},
            radar: {
                // shape: 'circle',
                name: {
                    textStyle: {
                        color: '#fff',
                        backgroundColor: '#999',
                        borderRadius: 3,
                        padding: [3, 5]
                    }
                },
                center: ['50%', '50%'],
                radius: 55,
                indicator: [
                    {name: '实用', max: 5},
                    {name: '趣味', max: 5},
                    {name: '易读', max: 5},
                    {name: '专业', max: 5},
                    {name: '装订', max: 5},
                ]
            },
            series: [{
                name: '图书评分',
                type: 'radar',
                areaStyle: {
                    normal: {
                        color: 'rgba(255, 240, 245, 1)'
                    }
                },
                // areaStyle: {normal: {}},
                data: [
                    {
                        value: [practicality, interesting, readability, professionalism, binding_quality],
                    }
                ]
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
    }
}

