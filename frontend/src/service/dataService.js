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
    
    // 增加超时时间到 10 分钟（600秒），因为 SVG 转换可能需要较长时间
    axios.post(url, param, {
        timeout: 600000  // 10 分钟超时
    })
    .then(response => {
        console.log("🟦 [Frontend] Response status:", response.status);
        console.log("🟦 [Frontend] Response data type:", typeof response.data);
        console.log("🟦 [Frontend] Response data keys:", Object.keys(response.data || {}));
        console.log("🟦 [Frontend] Response data preview:", response.data?.highlight?.substring(0, 50) || response.data?.substring(0, 50) || "No data");
        
        // 检查 SVG 内容
        if (response.data?.svg_content) {
            console.log("✅ [Frontend] SVG content received, length:", response.data.svg_content.length);
            console.log("✅ [Frontend] SVG content preview (first 200 chars):", response.data.svg_content.substring(0, 200));
        } else {
            console.warn("⚠️ [Frontend] No SVG content in response");
            if (response.data?.svg_path) {
                console.log("ℹ️ [Frontend] SVG path available:", response.data.svg_path);
            }
        }
        
        callback(response.data)
    }, errResponse => {
        console.error("❌ [Frontend] Error:", errResponse);
        if (errResponse.code === 'ECONNABORTED') {
            console.error("❌ [Frontend] Request timeout (请求超时)");
        } else if (errResponse.response) {
            console.error("❌ [Frontend] Response error:", errResponse.response.status, errResponse.response.data);
        } else {
            console.error("❌ [Frontend] Network error:", errResponse.message);
        }
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

export function ConvertToSvg(param, callback, errorCallback) {
    const url = `${T_URL}/convert_to_svg`;
    axios.post(url, param)
    .then(response => {
        if (callback) {
            callback(response.data);
        }
    }, errResponse => {
        console.error('Error converting to SVG:', errResponse);
        if (errorCallback) {
            errorCallback(errResponse);
        }
    })
}

export function startEvaluate(param, callback, errorCallback) {
    const url = `${T_URL}/evaluate_element`;
    axios.post(url, param)
    .then(response => {
        if (callback) {
            callback(response.data);
        }
    }, errResponse => {
        console.error('Error evaluating element:', errResponse);
        if (errorCallback) {
            errorCallback(errResponse);
        }
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

