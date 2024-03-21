<template>
  <div class="btns">
    <el-button type="primary" @click="outputJson">Output Json</el-button>
    <el-button type="success" @click="outputCsv">Output CSV</el-button>
    <el-button type="warning" @click="HueHistogram">HueHistogram</el-button>
  </div>
  <ul class="list" ref="listDom" :style="flag ? 'cursor:pointer': 'cursor:auto'">
    <li v-for="(item, index) in dataStore.barCodeList" @dblclick="showInfo(item, index)" :key="index" class="li" :style="{background: 'rgb(' + item+ ')'}"></li>
  </ul>
  <div class="content">
    <div class="mask" :style="isShow ? 'z-index:-1' : 'z-index: 1'"></div>
    <el-card style="min-width: calc((100% - 200px) / 3);" v-show="isShow" >
      <div class="square" :style="{background: info.rgb}"></div>
      <el-text class="mx-1" type="danger"><h3>R:</h3>{{info.R}}</el-text>
      <el-text class="mx-1" type="success"><h3>G:</h3>{{info.G}}</el-text>
      <el-text class="mx-1" type="primary"><h3>B:</h3>{{info.B}}</el-text>
    </el-card>
    <el-card style="min-width: calc((100% - 200px) / 3);" >
      <div id="myEcharts" ref="myEcharts"></div>
    </el-card>
    <el-card style="min-width: calc((100% - 200px) / 3);" v-show="isShow">
      <el-table :data="tableData" border style="width: 100%" :row-style="{height: '20px'}">
        <el-table-column prop="color" label="color" width="100">
          <template #default="{row}">
            <div :style="{background: row.color , width: '18px', height: '18px', border: '1px solid black'}"></div>
          </template>
        </el-table-column>
        <el-table-column prop="percentage" label="percentage"/>
        <el-table-column prop="colorName" label="colorName"/>
      </el-table>
    </el-card>
    <el-card style="min-width: calc((100% - 200px) / 3); margin-left: 20px;">
      <div id="myEcharts1" ref="myEcharts1"></div>
    </el-card>
    <el-card v-show="isShow" style="flex-grow: 1; margin-right: 20px; margin-left: 40px;">
      <div class="imgs">
        <el-image
            style="height: 100%"
            :src="'data:image/png;base64,'+info.url"
            fit="cover"></el-image>
      </div>
    </el-card>
  </div>

  <el-image-viewer
      v-if="showImagePreview"
      :zoom-rate="1.2"
      @close="closePreview"
      :url-list="imgPreviewList"
  />
</template>

<script setup lang="ts">

import  useHueHistogram from "@/hooks/useHueHistogram"
import  useBarcodeInfo from "@/hooks/useBarcodeInfo"
import {useDataStore} from "@/stores/data"
import {onMounted, ref} from "vue";

let { imgPreviewList, showImagePreview, closePreview, HueHistogram, outputJson, outputCsv } = useHueHistogram()
let { myEcharts, myEcharts1, info, showInfo, isShow, tableData } = useBarcodeInfo()
const dataStore = useDataStore()


const listDom = ref()

const flag = ref(false)
const downX = ref()
const scrollLeft = ref()

onMounted(()=>{
  sessionStorage.setItem("index", "0")
  dataStore.setBarCodeList(0)
  listDom.value.addEventListener("scroll", scrolling);
  listDom.value.addEventListener("mousedown", mousedown);
  listDom.value.addEventListener("mousemove", mousemove);
  listDom.value.addEventListener("mouseup", mouseup);
  listDom.value.addEventListener("mouseleave", mouseleave);
})



const scrolling=()=>{
  if(listDom.value.scrollLeft + listDom.value.clientWidth == listDom.value.scrollWidth){
    let index = Number(sessionStorage.getItem("index"))
    console.log(index)
    dataStore.setBarCodeList(index+1)
    sessionStorage.setItem("index", String(index+1))
  }
};

const mousedown=(event:any)=>{
  // console.log("mousedown")
  flag.value = true;
  downX.value = event.clientX; // 获取到点击的x下标
  scrollLeft.value = listDom.value.scrollLeft; // 获取当前元素滚动条的偏移量
};

const mousemove=(event:any)=>{
  // console.log("mousemove")
  if (flag.value) { // 判断是否是鼠标按下滚动元素区域
    let moveX = event.clientX; // 获取移动的x轴
    let scrollX = moveX - downX.value; // 当前移动的x轴下标减去刚点击下去的x轴下标得到鼠标滑动距离
    listDom.value.scrollLeft = scrollLeft.value - scrollX // 鼠标按下的滚动条偏移量减去当前鼠标的滑动距离
    // console.log(scrollX)
  }
};

const mouseup=()=>{
  // console.log("mouseup")
  flag.value = false;
};

const mouseleave=()=>{
  // console.log("mouseleave")
  flag.value = false;
};

</script>

<style scoped>
.el-col{
  display: flex;
  align-items: center;
  justify-content: space-around;
}
.el-card{
  height: 520px;
  box-sizing: border-box;
  border-radius: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
.list {
  max-width: 1280px;
  display: flex;
  height: 240px;
  flex-wrap: nowrap;
  overflow-x: auto;
  justify-content: flex-start;
  align-items: center;
  padding: 0;
  margin: 0;
  list-style: none;
  .li {
    width: 20px;
    height: 200px;
    flex-shrink: 0;
  }
  .li:hover{
    transition: 1s;
    transform: scale(1.2);
  }
}

.content{
  width: 100%;
  min-width: 1000px;
  margin: 20px auto;
  box-sizing: border-box;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  position: relative;
  .mask{
    width: 100%;
    height: 700px;
    position: absolute;
    background: white;
    top: -20px;
  }
  .square{
    width: 40px;
    height: 40px;
    display: inline-block;
    vertical-align: middle;
    margin-right: 10px;
  }
  .mx-1{
    margin: 0 10px;
    font-size: 22px;
    >h3{
      display: inline-block;
    }
  }
  .imgs{
    display: flex;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

}
#myEcharts{
  min-width: 400px;
  max-width: 800px;
  width: 100%;
  height: 400px;
}
#myEcharts1{
  min-width: 300px;
  max-width: 800px;
  width: 100%;
  height: 400px;
}
</style>
