import axios from 'axios';

// 后端服务器地址配置
// 方案1: 如果远程服务器直接暴露 HTTP 端口（需要配置 CORS）
// const T_URL = 'http://connect.westc.gpuhub.com:6006';
// 方案2: 通过 SSH 隧道访问（推荐，已建立隧道）
const T_URL = 'http://127.0.0.1:6006';
// 方案3: 如果后端在本地运行，使用：
// const T_URL = 'http://127.0.0.1:6006';

export function startBrainStorm(param, callback) {
    const url = `${T_URL}/brainstorm`;
    axios.post(`${url}?_=${Date.now()}`, param) //改动前：axios.post(url, param)
    .then(response => {
        callback(response.data)
    }, errResponnse => {
        console.log(errResponnse);
    })
}

export function imageSegment(param, callback) {
    console.log("🟦 [Frontend] image_url (first 100 chars):", param.image_url?.slice(0, 100));
    console.log("🟦 [Frontend] mode:", param.mode);
    console.log("🟦 [Frontend] Request URL:", `${T_URL}/image_segment`);
    const url = `${T_URL}/image_segment`;
    axios.post(url, param)
    .then(response => {
        console.log("🟦 [Frontend] Response status:", response.status);
        console.log("🟦 [Frontend] Response data type:", typeof response.data);
        console.log("🟦 [Frontend] Response data preview:", response.data?.highlight?.substring(0, 50) || response.data?.substring(0, 50) || "No data");
        callback(response.data)
    }, errResponnse => {
        console.error("❌ [Frontend] Error:", errResponnse);
    })
}

export function startImageExtract(param, callback) {
    const url = `${T_URL}/image_extract`;
    axios.post(url, param)
    .then(response => {
        callback(response.data)
    }, errResponnse => {
        console.log(errResponnse);
    })
}

export function startGenerate(param, callback) {
    const url = `${T_URL}/generate`;
    axios.post(url, param)
    .then(response => {
        callback(response.data)
    }, errResponnse => {
        console.log(errResponnse);
    })
}

export function startRetreiveInfo(param, callback) {
    const url = `${T_URL}/show_info`;
    axios.post(url, param)
    .then(response => {
        callback(response.data)
    }, errResponnse => {
        console.log(errResponnse);
    })
}

export function ConvertToSvg(param, callback) {
    const url = `${T_URL}/convert_to_svg`;
    axios.post(url, param)
    .then(response => {
        callback(response.data)
    }, errResponnse => {
        console.log(errResponnse);
    })
}

export function startEvaluate(param, callback) {
    const url = `${T_URL}/evaluate_element`;
    axios.post(url, param)
    .then(response => {
        callback(response.data)
    }, errResponnse => {
        console.log(errResponnse);
    })
}

export function startRefine(param, callback) {
    const url = `${T_URL}/refine_element`;
    axios.post(url, param)
    .then(response => {
        callback(response.data)
    }, errResponnse => {
        console.log(errResponnse);
    })
}

