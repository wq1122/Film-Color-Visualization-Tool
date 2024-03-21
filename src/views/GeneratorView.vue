<template>
  <el-form :model="form" label-width="auto" style="width: 1000px">
    <el-row>
      <el-col :span="8">
        <el-form-item label="Barcode Type">
          <el-select v-model="form.barcode_type">
            <el-option label="Color" value="Color"/>
            <el-option label="Brightness" value="Brightness"/>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="Frame Type">
          <el-select v-model="form.frame_type">
            <el-option label="Whole_frame" value="Whole_frame"/>
            <el-option label="Low_contrast_region" value="Low_contrast_region"/>
            <el-option label="High_contrast_region" value="High_contrast_region"/>
            <el-option label="Foreground" value="Foreground"/>
            <el-option label="Background" value="Background"/>
          </el-select>
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="Color Metric">
          <el-select v-model="form.color_metric">
            <el-option label="Average" value="Average"/>
            <el-option label="Median" value="Median"/>
            <el-option label="Mode" value="Mode"/>
            <el-option label="Top-dominant" value="Top-dominant"/>
            <el-option label="Weighted-dominant" value="Weighted-dominant"/>
            <el-option label="Bright" value="Bright"/>
            <el-option label="Brightest" value="Brightest"/>
          </el-select>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="11">
        <el-form-item label="multi_thread">
          <el-switch v-model="form.var_multi_thread" />
        </el-form-item>
      </el-col>
      <el-col :span="2"></el-col>
      <el-col :span="11">
        <el-form-item label="multi_thread">
          <el-input v-model="form.multi_thread" type="number"/>
        </el-form-item>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="11">
        <el-form-item label="saved_frame">
          <el-switch v-model="form.var_saved_frame" />
        </el-form-item>
      </el-col>
      <el-col :span="2"></el-col>
      <el-col :span="11">
        <el-form-item label="save_frames_rate">
          <el-input v-model="form.save_frames_rate" type="number"/>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="11">
        <el-form-item label="rescale_frame">
          <el-input v-model="form.var_rescale_frame" type="number"/>
        </el-form-item>
      </el-col>
      <el-col :span="2"></el-col>
      <el-col :span="11">
        <el-form-item label="rescale_factor">
          <el-input v-model="form.rescale_factor" type="number"/>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="11">
        <el-form-item label="letterbox_option">
          <el-radio-group v-model="form.letterbox_option">
            <el-radio value="Auto">Auto</el-radio>
            <el-radio value="Manual">Manual</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="6">
        <el-form-item label="high_ver">
          <el-input v-model="form.high_ver" type="number"/>
        </el-form-item>
      </el-col>
      <el-col :span="6">
        <el-form-item label="low_ver">
          <el-input v-model="form.low_ver" type="number"/>
        </el-form-item>
      </el-col>
      <el-col :span="6">
        <el-form-item label="left_hor">
          <el-input v-model="form.left_hor" type="number"/>
        </el-form-item>
      </el-col>
      <el-col :span="6">
        <el-form-item label="right_hor">
          <el-input v-model="form.right_hor" type="number"/>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-form-item label="unit_type">
        <el-radio-group v-model="form.unit_type">
          <el-radio value="Frame">Frame</el-radio>
          <el-radio value="Time">Time</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-row>
    <el-row>
      <el-col :span="8">
        <el-form-item label="total_frames_str">
          <el-input v-model="form.total_frames_str"/>
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="sampled_frame_rate_str">
          <el-input v-model="form.sampled_frame_rate_str"/>
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="skip_over_str">
          <el-input v-model="form.skip_over_str"/>
        </el-form-item>
      </el-col>
    </el-row>
    <el-row>
      <el-upload multiple action="" :on-change="handleChange" :auto-upload="false" :show-file-list="false">
        <el-form-item label="video_filename">
          <el-col :span="20"><el-input v-model="form.video_filename" disabled/></el-col>
          <el-col :span="4">
            <el-button>Browse</el-button>
          </el-col>
        </el-form-item>
      </el-upload>
    </el-row>
    <el-row>
      <el-col :span="8"></el-col>
      <el-col :span="8">
        <el-form-item>
          <el-button type="success" @click="onSubmit">Generator</el-button>
          <el-col :span="8"></el-col>
          <el-button type="primary" @click="settingDefault">Default Setting</el-button>
        </el-form-item>
      </el-col>
      <el-col :span="8"></el-col>
    </el-row>

  </el-form>
</template>

<script setup lang="ts">
import useFormInfo from "@/hooks/useFormInfo";
let {form, handleChange, settingDefault} = useFormInfo()
import {useDataStore} from "@/stores/data"
import {useRouter} from "vue-router";
const dataStore = useDataStore()
const router = useRouter()

const onSubmit = async () => {
  await dataStore.getData(form)
  await router.replace('/barcode')
}


</script>

<style scoped>

</style>
