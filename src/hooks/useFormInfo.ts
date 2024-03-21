import {reactive} from "vue";



export default function (){
    const form = reactive({
        barcode_type: 'Color',
        frame_type: 'Whole_frame',
        color_metric: 'Average',
        video_filename: '',
        var_multi_thread: true,
        multi_thread: 0,
        var_saved_frame: true,
        save_frames_rate: 0,
        var_rescale_frame: 1,
        rescale_factor: 0,
        letterbox_option: 'Auto',
        high_ver: 0,
        low_ver: 0,
        left_hor: 0,
        right_hor: 0,
        unit_type: 'Time',
        total_frames_str: '',
        sampled_frame_rate_str: '1',
        skip_over_str: ''
    })

    const handleChange = (uploadFile: any) => {
        form.video_filename = uploadFile.name;
    }

    const settingDefault = () => {
        form.barcode_type = 'Color';
        form.frame_type = 'Whole_frame';
        form.color_metric = 'Average';
        form.video_filename = '';
        form.var_multi_thread = true;
        form.multi_thread = 0;
        form.var_saved_frame = true;
        form.save_frames_rate = 0;
        form.var_rescale_frame = 1;
        form.rescale_factor = 0;
        form.letterbox_option = 'Auto';
        form.high_ver = 0;
        form.low_ver = 0;
        form.left_hor = 0;
        form.right_hor = 0;
        form.unit_type = 'Time';
        form.total_frames_str = '';
        form.sampled_frame_rate_str = '1';
        form.skip_over_str = '';
    }

    return {form, handleChange, settingDefault}
}