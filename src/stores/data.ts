import { defineStore } from 'pinia'
import {computed, reactive, ref} from "vue";
import {get, post} from "@/utils/api"

export const useDataStore = defineStore('data', () => {

    const data = ref()

    const barCodeList = ref<any>([])

    const setBarCodeList = async (index:number) => {
        if(index === 0){
            barCodeList.value = []
        }
        let tempList = null
        if(data.value){
            tempList= data.value['barcode']
        }else{
            const res = await get("/getJson")
            tempList = res['barcode']
        }

        let middleList:any = []
        for (let j = 0; j < tempList[0].length; j++) {
            for (let i = 0; i < tempList.length; i++) {
                middleList.push(tempList[i][j])
            }
        }
        let volume = 80
        let min = index * volume
        let max = Math.min((index + 1) * volume,middleList.length)
        for(let i = min; i < max; i++){
            barCodeList.value.push(middleList[i])
        }
    }
    const getData = async(form:object) => {
        const res = await post('/generateBarcode',form)
        // sessionStorage.setItem('data',JSON.stringify(res))
        sessionStorage.setItem("index", '0')
        data.value = res
    }

    const loadJson = async(filename:string) => {
        const res = await post('/getJson',{"json_filename":filename})
        // sessionStorage.setItem('data',JSON.stringify(res))
        sessionStorage.setItem("index", '0')
        data.value = res
    }

    return {data, barCodeList, setBarCodeList, getData, loadJson}

})