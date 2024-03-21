import {reactive, ref} from "vue";
import {get} from "@/utils/api";


export default function(){
    const imgPreviewList = ref<any>([])
    const showImagePreview = ref(false)
    const currentBase64FileData = reactive({
        base64: '',
        name: ''
    })

    const closePreview = () => {
        imgPreviewList.value = []
        showImagePreview.value = false
    }
    const HueHistogram = async ()=>{
        const res = await get("/getHueHistogram")
        currentBase64FileData.base64 = 'data:image/png;base64,' + res
        currentBase64FileData.name = "HueHistogram.png"
        showImagePreview.value = true
        imgPreviewList.value = [currentBase64FileData.base64]
    }

    const outputJson = async() => {
        const res = await get("/getJson");
        const jsonDataString = JSON.stringify(res);
        const blob = new Blob([jsonDataString], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "data.json";
        link.click();
    }

    const outputCsv = async() => {
        const res = await get("/getCSV");
        // const jsonDataString = JSON.stringify(res);
        const blob = new Blob([res], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "data.csv";
        link.click();
    }

    return {imgPreviewList, showImagePreview, closePreview, HueHistogram, outputJson, outputCsv}
}