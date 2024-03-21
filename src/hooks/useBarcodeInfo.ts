import {reactive, ref} from "vue";
import * as echarts from "echarts";
import {get, post} from "@/utils/api";

export default function (){
    let chart:any = null
    let chart1:any = null
    let myEcharts= ref()
    let myEcharts1= ref()
    const tableData = reactive<any>([])
    const isShow = ref(false)
    function initChart() {
        if(!chart){
            chart = echarts.init(myEcharts.value,'light');
            chart1 = echarts.init(myEcharts1.value,'light');
        }
        // 把配置和数据放这里
        chart.setOption({
            title: {
                text: 'dominant colors',
                left: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: '{b}: ({d}%)'
            },
            legend: {
                top: "20px",
                left: 'center'
            },
            color:['black', 'brown', 'grey', 'red', 'orange', 'blue', 'cyan', 'magenta', 'white', 'yellow', 'green'],
            series: [
                {
                    name: 'Access From',
                    type: 'pie',
                    radius: '40%',
                    data: info.list,
                    labelLine: {
                        show: false
                    },
                    label: {
                        show: false,
                        position: 'center'
                    },
                },
                {
                    type: 'pie',
                    clockWise: false,
                    radius: ['40%','41%'],
                    data: [10],
                    labelLine: {
                        show: false
                    }
                },
            ]
        });
        chart1.setOption({
            title: {
                text: 'color harmony',
                left: 'center'
            },
            toolbox: {
                show: true,
                feature: {
                    restore: { show: true },
                    saveAsImage: { show: true }
                }
            },
            color:['#FF0000','#FF3F00','#FF7F00','#FFBF00','#FFFF00','#BFFF00',
                '#7FFF00','#3FFF00','#00FF00','#00FF3F','#00FF7F','#00FFBF',
                '#00FFFF','#00BFFF','#007FFF','#003FFF','#0000FF','#3F00FF',
                '#7F00FF','#BF00FF','#FF00FF','#FF00BF','#FF007F','#FF003F'
            ],
            series: [
                {
                    name: 'Nightingale Chart',
                    type: 'pie',
                    roseType: 'radius',
                    label: {
                        show: false
                    },
                    itemStyle: {
                        borderRadius: 6
                    },
                    radius: '100%',
                    data: info.list1
                }
            ]
        });
        window.onresize = function() {
            chart1.resize();
            //自适应大小
            chart.resize();

        };
    }
    const info = reactive({
        R: 0,
        G: 0,
        B: 0,
        rgb: '',
        url: '',
        list:[],
        list1:[]
    })
    const showInfo = async(item:Array<number>, index:number)=>{
        const res = await post("/getColorDominant",{"which":index})
        const res2 = await post("/getImgBase64", {"which":index})
        const res3 = await post("/getColorHighlight", {"which":index})
        info.rgb = 'rgb('+item[0]+','+item[1]+','+item[2]+')'
        info.R = Number(item[0].toFixed(2))
        info.G = Number(item[1].toFixed(2))
        info.B = Number(item[2].toFixed(2))
        info.url = res2
        info.list = res
        info.list1 = res3
        initChart()
        tableData.splice(0,tableData.length)
        let sum:number = 0
        for(let i = 0; i < res.length; i++){
            sum += Number(res[i].value)
        }
        for(let i = 0; i < res.length; i++){
            tableData.push({
                color: res[i].name,
                percentage: ((res[i].value/sum)*100).toFixed(2)+'%',
                colorName: res[i].name
            })
        }
        isShow.value = true
    }

    return {myEcharts,myEcharts1, info, showInfo, isShow, tableData}
}