<template>
    <div class="header">
      <el-menu :default-active="activeIndex" class="el-menu-demo" background-color="#545c64"
               text-color="#fff" active-text-color="#ffd04b" mode="horizontal" @select="handleSelect">
        <el-menu-item index="1">Generate BarCode</el-menu-item>
        <el-menu-item index="2">Load Json</el-menu-item>
        <el-menu-item index="3">BarCode</el-menu-item>
      </el-menu>
    </div>
  <div class="content">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'
import {ref, watch} from 'vue'
const router = useRouter()
const activeIndex = ref('1')
const handleSelect = (key:string) => {
  switch (key){
    case '1':
      router.replace('/generator')
      break
    case '2':
      router.replace('/load')
      break
    case '3':
      router.replace('/barcode')
      break
    default:
      router.replace('/barcode')
      break
  }
}


</script>

<style scoped lang="less">
.header {
  max-width: 1280px;
  width: 100%;
  height: 60px;
}
.content{
  margin-top: 40px;
  max-width: 1280px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
