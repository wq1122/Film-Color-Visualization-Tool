<template>
  <el-upload
      class="upload-demo"
      drag
      action=""
      accept="json"
      :limit="1"
      :on-change="beforeUpload"
      :auto-upload="false"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        json files
      </div>
    </template>
  </el-upload>
  <el-button type="primary" @click="loadJson">Generate</el-button>
</template>

<script setup lang="ts">
import { UploadFilled } from '@element-plus/icons-vue'
import {useDataStore} from "@/stores/data"
import { ElMessage } from 'element-plus'
import {useRouter} from "vue-router";
const dataStore = useDataStore()
const router = useRouter()

let filename = null
const beforeUpload = (file)=>{
  filename = file.name
}
const loadJson = async ()=>{
  let type = filename.split('.')[1]
  const isJson = type === 'json';
  if (!isJson) {
    ElMessage({
      message: "文件格式错误！",
      type: 'warning'
    })
    return
  }
  await dataStore.loadJson(filename)
  await router.replace('/barcode')
}
</script>

<style scoped>

</style>