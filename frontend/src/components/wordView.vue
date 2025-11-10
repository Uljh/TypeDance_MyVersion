<!--
 * @Author: 秦少卫
 * @Date: 2022-09-03 19:16:55
 * @LastEditors: 秦少卫
 * @LastEditTime: 2022-09-06 23:20:40
 * @Description: 图层面板
-->

<template>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

  <div class="ideaView">
    <h3>
      <button class="title-btn">
        <svg t="1690124817154" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="11543">
          <path
            d="M511.788986 108.889278a32.666783 32.666783 0 0 0 32.666784-32.666783v-43.555712a32.666783 32.666783 0 0 0-65.333567 0v43.555712a32.666783 32.666783 0 0 0 32.666783 32.666783zM969.123955 413.997036h-43.555711a32.666783 32.666783 0 0 0 0 65.333567h43.555711a32.666783 32.666783 0 0 0 0-65.333567zM130.676512 446.66382A32.797451 32.797451 0 0 0 98.009729 413.997036h-43.555711a32.666783 32.666783 0 0 0 0 65.333567h43.555711A32.666783 32.666783 0 0 0 130.676512 446.66382z m768.758305 258.938704a28.986326 28.986326 0 0 0-41.63926 0 29.922774 29.922774 0 0 0 0 42.031261l27.788544 28.093434a29.574328 29.574328 0 0 0 41.63926-42.031262zM130.676512 692.753589l-30.815665 31.142333a33.407231 33.407231 0 0 0 0 46.82239 32.666783 32.666783 0 0 0 46.190831 0l30.815666-31.142334a33.145896 33.145896 0 0 0 0-46.604611 32.29656 32.29656 0 0 0-46.081942-0.217778z m696.891382-170.085053A308.025991 308.025991 0 0 0 517.516563 217.560778 297.529064 297.529064 0 0 0 217.657268 518.748522a304.084199 304.084199 0 0 0 155.472111 273.747646 39.875254 39.875254 0 0 0-3.157789 28.311212v67.729131c0 74.698045 52.114409 135.458262 125.396893 135.458262h44.296159A134.325814 134.325814 0 0 0 675.122904 893.109861v-65.333567a64.985121 64.985121 0 0 0-10.475149-35.280126A305.325536 305.325536 0 0 0 827.567894 522.668536zM609.789337 827.776294v21.777855h-114.35552a32.666783 32.666783 0 1 0 0 65.333567h110.348395a70.974032 70.974032 0 0 1-66.052237 43.77349h-44.296158c-36.695687 0-59.82377-32.666783-59.82377-70.124695v-67.729131l81.754071 6.968914H609.789337z m-91.989662-65.333567h-0.435557A238.685298 238.685298 0 0 1 283.121502 518.748522a231.651051 231.651051 0 0 1 234.438616-235.636398A239.687079 239.687079 0 1 1 517.734341 762.442727z m-0.217779-424.885964a32.666783 32.666783 0 1 0 0 65.333567 120.997766 120.997766 0 0 1 121.803547 119.778206 33.233008 33.233008 0 0 0 66.444237 0 186.875779 186.875779 0 0 0-188.313117-185.111773z m382.027144 368.045761a28.986326 28.986326 0 0 0-41.63926 0 29.922774 29.922774 0 0 0 0 42.031261l27.788544 28.093434a29.574328 29.574328 0 0 0 41.63926-42.031262z m-768.758305-12.848935l-30.815666 31.142333a33.407231 33.407231 0 0 0 0 46.82239 32.666783 32.666783 0 0 0 46.190832 0l30.815666-31.142334a33.145896 33.145896 0 0 0 0-46.604611 32.29656 32.29656 0 0 0-46.256165-0.217778zM823.081655 122.827106l-32.165892 32.884562a35.323682 35.323682 0 0 0 0 49.217954 33.51612 33.51612 0 0 0 48.216172 0l32.144115-32.884562a35.280126 35.280126 0 0 0 0-49.217954 33.537898 33.537898 0 0 0-48.259728 0z m-651.157884-2.831121l34.844569 34.844569a36.913465 36.913465 0 1 1-52.114409 52.266853l-34.844569-34.844569A36.957021 36.957021 0 0 1 172.054438 119.995985z"
            p-id="11544"></path>
        </svg>
      </button>
      <span>IDEATION ---------------------</span>
    </h3>

    <div class="idea-input" style="display: flex; align-items: center; padding-left: 10px; ">
      <form>
        <textarea placeholder="Describe the concept" rows="20" name="idea" id="idea" cols="40" class="text-idea"
          autocomplete="off" role="textbox" aria-autocomplete="list" aria-haspopup="true"></textarea>
      </form>
      <button class="button-idea" @click="clickBrainstorm">Brain
        storm</button>
    </div>
    <ul class="tags" style="padding-left: 10px;">
      <el-tooltip effect="light" placement="top-start" :content="ttipContent1">
        <li>
          <a href="#" class="tag" id="tag-concept1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>
        </li>
      </el-tooltip>

      <el-tooltip effect="light" placement="top-start" :content="ttipContent2">
        <li>
          <a href="#" class="tag" id="tag-concept2">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>
        </li>
      </el-tooltip>

      <el-tooltip effect="light" placement="top-start" :content="ttipContent3">
        <li>
          <a href="#" class="tag" id="tag-concept3">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>
        </li>
      </el-tooltip>

      <el-tooltip effect="light" placement="top-start" :content="ttipContent4">
        <li>
          <a href="#" class="tag" id="tag-concept4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>
        </li>
      </el-tooltip>

      <el-tooltip effect="light" placement="top-start" :content="ttipContent5">
        <li>
          <a href="#" class="tag" id="tag-concept5">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</a>
        </li>
      </el-tooltip>


    </ul>

  </div>

  <div class="wordView">
    <h3>
      <button class="title-btn">
        <svg t="1690097700978" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="6347">
          <path
            d="M853.333333 1024 170.666667 1024c-93.866667 0-170.666667-76.8-170.666667-170.666667L0 170.666667c0-93.866667 76.8-170.666667 170.666667-170.666667l682.666667 0c93.866667 0 170.666667 76.8 170.666667 170.666667l0 682.666667C1024 947.2 947.2 1024 853.333333 1024zM170.666667 85.333333C123.733333 85.333333 85.333333 123.733333 85.333333 170.666667l0 682.666667c0 46.933333 38.4 85.333333 85.333333 85.333333l682.666667 0c46.933333 0 85.333333-38.4 85.333333-85.333333L938.666667 170.666667c0-46.933333-38.4-85.333333-85.333333-85.333333L170.666667 85.333333z"
            p-id="6348">
          </path>
          <path
            d="M725.333333 341.333333 298.666667 341.333333C273.066667 341.333333 256 324.266667 256 298.666667s17.066667-42.666667 42.666667-42.666667l426.666667 0c25.6 0 42.666667 17.066667 42.666667 42.666667S750.933333 341.333333 725.333333 341.333333z"
            p-id="6349"></path>
          <path
            d="M298.666667 384C273.066667 384 256 366.933333 256 341.333333L256 298.666667c0-25.6 17.066667-42.666667 42.666667-42.666667s42.666667 17.066667 42.666667 42.666667l0 42.666667C341.333333 366.933333 324.266667 384 298.666667 384z"
            p-id="6350"></path>
          <path
            d="M725.333333 384c-25.6 0-42.666667-17.066667-42.666667-42.666667L682.666667 298.666667c0-25.6 17.066667-42.666667 42.666667-42.666667s42.666667 17.066667 42.666667 42.666667l0 42.666667C768 366.933333 750.933333 384 725.333333 384z"
            p-id="6351"></path>
          <path
            d="M512 768c-25.6 0-42.666667-17.066667-42.666667-42.666667L469.333333 298.666667c0-25.6 17.066667-42.666667 42.666667-42.666667s42.666667 17.066667 42.666667 42.666667l0 426.666667C554.666667 750.933333 537.6 768 512 768z"
            p-id="6352"></path>
          <path
            d="M554.666667 768l-85.333333 0c-25.6 0-42.666667-17.066667-42.666667-42.666667s17.066667-42.666667 42.666667-42.666667l85.333333 0c25.6 0 42.666667 17.066667 42.666667 42.666667S580.266667 768 554.666667 768z"
            p-id="6353">
          </path>
        </svg>
        <!-- <svg t="1690097451111" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="5328">
          <path d="M640 512a128 128 0 1 0 0-256 128 128 0 0 0 0 256z m0-64a64 64 0 1 0 0-128 64 64 0 0 0 0 128z" p-id="5329">
          </path>
          <path d="M128 832a64 64 0 0 0 64 64h640a64 64 0 0 0 64-64V192a64 64 0 0 0-64-64H192a64 64 0 0 0-64 64v640z m64-82.752l192-192L658.752 832H192v-82.752z m0-90.496V192h640v640h-82.752L384 466.752l-192 192z" p-id="5330">
        </path></svg> -->
      </button>
      <span>Typeface ---------------------</span>
    </h3>

    <div class="word-input" style="display: inline-block; padding-left: 10px; ">
      <form>
        <textarea placeholder="Input the word" rows="20" name="object" id="object" cols="40" class="text-word"
          autocomplete="off" role="textbox" aria-autocomplete="list" aria-haspopup="true"></textarea>
      </form>
      <div class="word-options">
        <!-- <button class="inline-button" @click="changeFont">Font Type ▼</button> -->
        <el-select class="inline-button" placeholder="Font type" style="width: 39%;" v-model="selectedFont">
          <el-option v-for="item in fontFamilyList" :value="item" :key="'font-' + item">{{ item }}</el-option>
        </el-select>
        <button class="inline-button" @click="displayText">Display</button>
        <button class="inline-button" id="addButton" @click="addSelectionTrigger" style="width: fit-content;">
          <svg t="1694243217565" class="icon-function" style="width: 12px;" viewBox="0 0 1024 1024" version="1.1"
            xmlns="http://www.w3.org/2000/svg" p-id="9676">
            <path d="M992 464H560V32h-96v432H32v96h432v432h96V560h432z" p-id="9677"></path>
          </svg>
        </button>
        <button class="inline-button" id="confirmButton" @click="displayTextOnCanvas" style="width: 42px;">
          <svg t="1690350488185" class="icon-function" viewBox="0 0 1024 1024" version="1.1"
            xmlns="http://www.w3.org/2000/svg" p-id="37475">
            <path
              d="M346.595344 684.495656 135.774825 473.675136l-71.492264 71.447239 282.312784 282.268782 606.406137-606.358041-71.447239-71.492264L346.595344 684.495656z"
              p-id="37476"></path>
          </svg>
        </button>
      </div>

      <canvas id="canva-word" width="232" height="150"></canvas>
    </div>
  </div>

  <div class="imageView">
    <h3>
      <button class="title-btn">
        <svg t="1690097881001" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg"
          p-id="7490">
          <path d="M416 266.538667m-96 0a96 96 0 1 0 192 0 96 96 0 1 0-192 0Z" p-id="7491"></path>
          <path
            d="M721.749333 371.626667A43.818667 43.818667 0 0 0 682.666667 348.074667a42.965333 42.965333 0 0 0-38.058667 25.002666l-66.474667 146.517334a10.624 10.624 0 0 1-18.005333 2.261333l-34.986667-43.690667a42.666667 42.666667 0 0 0-34.688-16.042666 42.965333 42.965333 0 0 0-33.578666 18.176L323.84 670.293333a21.333333 21.333333 0 0 0 17.493333 33.706667h512a21.333333 21.333333 0 0 0 18.133334-10.112 21.333333 21.333333 0 0 0 0.938666-20.736z"
            p-id="7492"></path>
          <path
            d="M938.666667 0H234.666667a85.333333 85.333333 0 0 0-85.333334 85.333333v704a85.333333 85.333333 0 0 0 85.333334 85.333334H938.666667a85.333333 85.333333 0 0 0 85.333333-85.333334V85.333333a85.333333 85.333333 0 0 0-85.333333-85.333333z m-6.186667 783.104a21.333333 21.333333 0 0 1-15.104 6.229333H256a21.333333 21.333333 0 0 1-21.333333-21.333333V106.666667A21.333333 21.333333 0 0 1 256 85.333333h661.333333a21.333333 21.333333 0 0 1 21.333334 21.333334V768a21.333333 21.333333 0 0 1-6.186667 14.976z"
            p-id="7493"></path>
          <path
            d="M832 938.666667h-725.333333a21.333333 21.333333 0 0 1-21.333334-21.333334v-725.333333a42.666667 42.666667 0 0 0-85.333333 0V938.666667a85.333333 85.333333 0 0 0 85.333333 85.333333h746.666667a42.666667 42.666667 0 0 0 0-85.333333z"
            p-id="7494"></path>
        </svg>
      </button>
      <span>IMAGERY ---------------------</span>
    </h3>

    <div class="img-input" style="display: flex; align-items: center; padding-left: 10px; ">
      <div class="upload-img-container" style="display: flex; flex-direction: column; padding-left: 10px;">
        <button class="upload-img" @click="loadImageOrDisplay1">
          <img id="img1" width="50" height="50" src="src\assets\upload_image\default1.png">
          <input id="input-img1" type="file" name="contact_image_1" />
        </button>
        <button class="upload-img" @click="loadImageOrDisplay2">
          <img id="img2" width="50" height="50" src="src\assets\upload_image\default1.png"></button>
        <input id="input-img2" type="file" name="contact_image_1" />
        <button class="upload-img" @click="loadImageOrDisplay3">
          <img id="img3" width="50" height="50" src="src\assets\upload_image\default1.png"></button>
        <input id="input-img3" type="file" name="contact_image_1" />
        <!-- <div class="img-button-container" style="display: flex; justify-content: space-between; margin-right: 5px;"> -->
        <!-- <button class="lassoButton-img" id="lassoButton-img">
          <svg t="1690350605083" class="icon-function-small" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="42621" >
            <path d="M351.866914 645.910768c-43.577233 0-85.884838-8.547496-125.723167-25.39256-38.458733-16.265235-72.998614-39.548414-102.63993-69.199727-29.651313-29.651313-52.924495-64.181197-69.199726-102.63993-16.855062-39.838329-25.392561-82.145934-25.392561-125.723167s8.547496-85.884838 25.392561-125.723167c16.265235-38.458733 39.548414-72.998614 69.199726-102.63993 29.651313-29.651313 64.181197-52.924495 102.63993-69.199726C265.982076 8.537499 308.289681 0 351.866914 0s85.884838 8.547496 125.723167 25.392561c38.458733 16.265235 72.998614 39.548414 102.63993 69.199726 29.651313 29.651313 52.924495 64.181197 69.199726 102.63993 16.855062 39.838329 25.392561 82.145934 25.392561 125.723167 0 21.883589-2.209353 43.767178-6.558079 65.040945l-77.647251-15.885346c3.289036-16.055296 4.94855-32.600449 4.94855-49.155599 0-134.380631-109.32797-243.708601-243.708601-243.708601S108.158313 188.574753 108.158313 322.955384 217.486283 566.663985 351.866914 566.663985c16.495167 0 32.980338-1.649517 48.985649-4.918559l15.83536 77.657249c-21.213785 4.318735-43.017397 6.508093-64.821009 6.508093z" fill="#333333" p-id="42622"></path><path d="M904.345055 563.674861L533.173797 893.248306 371.491165 337.351167zM725.547437 722.428351L966.186937 997.607732" fill="#333333" p-id="42623"></path><path d="M695.754166 748.540701l59.66452-52.174714 240.643499 275.187378-59.66452 52.174715z" p-id="42624"></path>
          </svg>
        </button> -->
        <button class="lassoButton-img" id="lassoButton-img" @click="startExtract">
          <svg t="1690350488185" class="icon-function-small" viewBox="0 0 1024 1024" version="1.1"
            xmlns="http://www.w3.org/2000/svg" p-id="37475">
            <path
              d="M346.595344 684.495656 135.774825 473.675136l-71.492264 71.447239 282.312784 282.268782 606.406137-606.358041-71.447239-71.492264L346.595344 684.495656z"
              p-id="37476"></path>
          </svg>
        </button>
        <!-- </div> -->
      </div>
      <canvas id="canva-img" width="180" height="180"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue';
import { useRouter, useRoute } from 'vue-router'
import { useSettingStore, useJsonStore } from '../store/modules/settingStore'
import { useDesignPriorStore } from '../store/modules/imageViewStore'
import { startBrainStorm, imageSegment, startImageExtract } from '../service/dataService';

// 获取后端服务器地址（与 dataService.js 中的 T_URL 保持一致）
// 注意：这里需要与 dataService.js 中的配置保持一致
const BACKEND_URL = 'http://127.0.0.1:6006';
import fontList from "@/assets/fonts/font";
import { fabric } from 'fabric';

const canvas = inject("canvas")
const storeDesignPrior = useDesignPriorStore()
const eventBus = inject("eventBus")

// // =================== ABOUT LASSO ==========================
// Lasso 选区模式（旧逻辑，现已废弃，使用拖拽选区代替）

// =================== ABOUT FONT ==========================
let fontFamilyList = ref(fontList.map(item => item.fontFamily))
let selectedFont = ref("Arial")
let firstDisplayWord = ref(true)
let addSelection = ref(false)
let select_boxes = ref([])
let current_box = ref([])

function displayText() {
  var textarea = document.getElementById("object");
  // delete old canvas
  var oldCanvas = document.getElementById("canva-word");

  if (firstDisplayWord.value) {
    oldCanvas.parentNode.removeChild(oldCanvas);
    firstDisplayWord.value = false
  }
  else {
    var parentElement = oldCanvas.parentNode;
    var grandparentElement = parentElement.parentNode;
    grandparentElement.removeChild(parentElement);

    // clear cache
    addSelection.value = false;
    select_boxes.value = []
  }

  // add new canvas
  const imgInputDiv = document.querySelector(".word-input");
  const canvasWord0 = document.createElement("canvas")

  canvasWord0.id = "canva-word";
  canvasWord0.width = 232;
  canvasWord0.height = 150;
  imgInputDiv.appendChild(canvasWord0);

  // add style for canvas
  const style = document.createElement("style");
  style.innerHTML = `
  .canvas-container {
    background-color: #ffffff;
    padding: 5px 8px;
    border-radius: 6px;
    border: 1px solid #cacaca; }`;
  document.head.appendChild(style);

  const canvasWord = new fabric.Canvas('canva-word', { backgroundColor: "white" });
  // canvasWord.setWidth(232);
  // canvasWord.setHeight(150);
  canvasWord.renderAll()

  var ctx = canvasWord.getContext("2d");
  // Clear the canvas
  ctx.clearRect(0, 0, 232, 150);

  // Set the maximum font size and position
  var maxFontSize = 130;
  var x = 232 / 2;
  var y = 150 / 2;

  // Get the text from the textarea
  var text = textarea.value;

  // Set the initial font size
  var fontSize = maxFontSize;

  // Decrease the font size until the text fits within the canvas
  do {
    // Set the font and text color
    ctx.font = fontSize + "px Times New Roman";
    ctx.fillStyle = "black";

    // Measure the width of the text
    var textWidth = ctx.measureText(text).width + 25;
    // Decrease the font size
    fontSize--;

    // Break the loop if the font size becomes too small
    if (fontSize <= 0) {
      break;
    }
  } while (textWidth > canvasWord.width);
  ctx.font = fontSize + "px Times New Roman";
  ctx.fillStyle = "black";
  let textHeight = ctx.measureText(text).actualBoundingBoxAscent;
  // Set the final font size and position
  ctx.font = fontSize + "px " + selectedFont.value;
  x -= (textWidth / 2);
  y -= ((textHeight / 2) + 10);

  // Display the text on the canvas
  // ctx.fillText(text, x, y);
  const textInstance = new fabric.IText(text, {
    left: x,
    top: y,
    fontSize: fontSize,
    fill: 'black',
    fontFamily: selectedFont.value,
  });
  textInstance.selectable = false;
  canvasWord.add(textInstance);

  // free draw rectangle
  var rectangle, isDown, origX, origY;

  canvasWord.on('mouse:down', function (o) {
    var pointer = canvasWord.getPointer(o.e);

    isDown = true;
    origX = pointer.x;
    origY = pointer.y;

    rectangle = new fabric.Rect({
      left: origX,
      top: origY,
      fill: 'transparent',
      // stroke: '#6cffd6',
      // stroke: '#797B0B',
      strokeWidth: 0,
    });
    rectangle.selectable = false
    canvasWord.add(rectangle);
  });

  canvasWord.on('mouse:move', function (o) {
    if (!isDown) return;
    var pointer = canvasWord.getPointer(o.e);
    if (origX > pointer.x) {
      rectangle.set({ left: Math.abs(pointer.x) });
    }
    if (origY > pointer.y) {
      rectangle.set({ top: Math.abs(pointer.y) });
    }

    rectangle.set({ width: Math.abs(origX - pointer.x) });
    rectangle.set({ height: Math.abs(origY - pointer.y) });
    canvasWord.renderAll();
  });

  // ✅ 鼠标释放事件：处理字体笔画选区 + 同步中央 SVG
    canvasWord.on('mouse:up', function (o) {
      isDown = false;
      const option = { format: 'png', quality: 2, multiplier: 2 };
      const dataUrl = canvasWord.toDataURL(option);
      current_box.value = [
        rectangle.left * 2,
        rectangle.top * 2,
        (rectangle.left + rectangle.width) * 2,
        (rectangle.top + rectangle.height) * 2
      ];

      // 封装参数
      let param;
      if (addSelection.value === true) {
        select_boxes.value.push(current_box.value);
        param = {
          box: select_boxes.value,
          image_url: dataUrl,
          mode: "word"
        };
      } else {
        param = {
          box: current_box.value,
          image_url: dataUrl,
          mode: "word"
        };
      }

      console.log("📤 Sending param to /image_segment:", param);

      // 调用后端接口
      imageSegment(param, function (data) {
        console.log("✅ [WORD Mode] Received data from backend:", data);
        console.log("✅ [WORD Mode] data.highlight exists:", !!data.highlight);
        console.log("✅ [WORD Mode] data.highlight preview:", data.highlight?.substring(0, 50) + "...");

        // ========== 左侧 Canvas：显示高亮选区 ==========
        const imgEl = document.createElement('img');
        if (!data.highlight) {
          console.error("❌ No highlight data received from backend");
          return;
        }
        // 确保使用最新的 base64 数据，避免缓存问题
        // 由于 base64 data URL 包含了完整的数据，不需要担心缓存
        // 但为了确保显示最新内容，我们直接使用返回的数据
        imgEl.src = data.highlight; // 后端返回的高亮部分（DataURL）
        imgEl.crossOrigin = "anonymous"; // 避免跨域问题
        document.body.appendChild(imgEl);
        console.log("✅ [WORD Mode] Image element created, src length:", data.highlight.length);

        imgEl.onload = () => {
          console.log("✅ [WORD Mode] Image loaded, dimensions:", imgEl.width, "x", imgEl.height);
          // 完全清除 canvas，确保显示最新内容
          canvasWord.clear();
          canvasWord.backgroundColor = "white"; // 确保背景色
          
          const imgInstanceNew = new fabric.Image(imgEl, { left: 0, top: 0 });
          imgInstanceNew.scaleToWidth(canvasWord.getWidth());
          imgInstanceNew.scaleToHeight(canvasWord.getHeight());
          imgInstanceNew.selectable = false;
          canvasWord.add(imgInstanceNew);
          canvasWord.renderAll();
          console.log("✅ [WORD Mode] Image added to canvas and rendered");
          imgEl.remove();
        };
        
        imgEl.onerror = (error) => {
          console.error("❌ [WORD Mode] Failed to load image:", error);
          console.error("❌ [WORD Mode] Image src preview:", data.highlight.substring(0, 100));
        };

        // ========== 中央主画布：加载剩余结构（SVG） ==========
        // 优先使用后端返回的 SVG 内容（直接字符串），如果没有则尝试从路径加载
        console.log("🎨 [SVG] Checking SVG data in response...");
        console.log("🎨 [SVG] data keys:", Object.keys(data || {}));
        console.log("🎨 [SVG] data.svg_content exists:", !!data.svg_content);
        console.log("🎨 [SVG] data.svg_path exists:", !!data.svg_path);
        
        if (data.svg_content) {
          console.log("✅ [SVG] Loading SVG from content (length):", data.svg_content.length);
          console.log("✅ [SVG] SVG content preview (first 200 chars):", data.svg_content.substring(0, 200));
          try {
            displayTextOnCanvasFromString(data.svg_content);
          } catch (error) {
            console.error("❌ [SVG] Error calling displayTextOnCanvasFromString:", error);
          }
        } else if (data.svg_path) {
         console.log("⚠️ [SVG] No SVG content, loading from path:", data.svg_path);
         console.log("ℹ️ [SVG] 前端将等待新的 SVG 文件生成（文件将被覆盖，通过文件大小变化检测新文件）");
          
          // ⚠️ 重要：将相对路径转换为完整的后端 URL
          // 后端返回的路径是相对路径（如 /api/svg_image/...），需要添加后端服务器地址
          // 后端服务器地址：http://127.0.0.1:6006
          const BACKEND_URL_LOCAL = 'http://127.0.0.1:6006';
          let svgPath = String(data.svg_path);
          
          console.log(`🔍 [SVG] 原始路径: ${svgPath}`);
          console.log(`🔍 [SVG] BACKEND_URL: ${BACKEND_URL_LOCAL}`);
          
          // 如果路径是相对路径（以 / 开头），添加后端服务器地址
          if (svgPath.startsWith('/')) {
            svgPath = BACKEND_URL_LOCAL + svgPath;
            console.log(`✅ [SVG] 相对路径转换为完整 URL: ${svgPath}`);
          } else if (svgPath.startsWith('http://') || svgPath.startsWith('https://')) {
            // 如果已经是完整 URL，直接使用
            console.log(`✅ [SVG] 路径已是完整 URL: ${svgPath}`);
          } else {
            // 如果不是完整 URL 也不是相对路径，添加后端服务器地址
            svgPath = BACKEND_URL_LOCAL + '/' + svgPath;
            console.log(`✅ [SVG] 其他路径转换为完整 URL: ${svgPath}`);
          }
          
          console.log(`✅ [SVG] 后端返回的路径: ${data.svg_path}`);
          console.log(`✅ [SVG] 最终使用的完整 SVG URL: ${svgPath}`);
          
         // 记录开始等待的时间，用于检测新文件
         // ⚠️ 关键：记录请求开始时间，只有修改时间晚于开始时间的文件才是新文件
         const startTime = Date.now();
         const requestStartTime = startTime; // 请求开始时间，用于判断文件是否是新生成的
         let lastModifiedTime = null;
         let lastFileSize = 0;
         let initialFileSize = 0; // 初始文件大小
         let initialModifiedTime = null; // 初始文件修改时间
         let stableFileSizeCount = 0; // 文件大小稳定的次数（连续两次检查大小一致）
         let loadSuccess = false;
         let initialFileDetected = false; // 是否已经检测到初始文件（可能是旧文件）
         
         // 如果 SVG 内容不存在，尝试从路径加载
         // ⚠️ 关键逻辑：只有文件的修改时间晚于请求开始时间，或者文件大小发生变化，才认为是新文件
         // 使用轮询机制等待新文件生成
         let retryCount = 0;
         const maxRetries = 180; // 最多重试180次（180秒，3分钟），因为SVG转换可能需要更长时间
         const retryInterval = 1000; // 每1秒重试一次
         
         function tryLoadSVG() {
           if (loadSuccess) {
             console.log("✅ [SVG] SVG 已成功加载，停止重试");
             return;
           }
           
           retryCount++;
           const currentTime = Date.now();
           const elapsedTime = ((currentTime - startTime) / 1000).toFixed(1);
           
           // 每次请求都添加新的时间戳，避免浏览器缓存
           const svgUrl = svgPath + "?t=" + currentTime + "&v=" + Math.random();
           console.log(`🔄 [SVG] 检查 SVG 文件 (${retryCount}/${maxRetries}, ${elapsedTime}s):`, svgUrl);
           
           // 使用 fetch 先检查文件是否存在，并获取文件信息
           // 注意：不手动添加缓存控制头，避免 CORS 问题
           // URL 中的时间戳和随机数已经可以避免浏览器缓存
           // 使用 HEAD 请求检查文件是否存在和获取文件信息
           // 注意：不添加任何自定义请求头，避免 CORS 预检请求问题
           fetch(svgUrl, { 
             method: 'HEAD',
             mode: 'cors'
           })
             .then(response => {
               if (response.ok) {
                 // 检查文件大小和修改时间
                 const contentLength = response.headers.get('content-length');
                 const lastModified = response.headers.get('last-modified');
                 const fileSize = contentLength ? parseInt(contentLength) : 0;
                 const modifiedTime = lastModified ? new Date(lastModified).getTime() : null;
                 
                 const elapsedSeconds = (Date.now() - startTime) / 1000;
                 const fileTime = modifiedTime;
                 const timeDiff = fileTime ? fileTime - requestStartTime : 0;
                 
                 console.log(`ℹ️ [SVG] 文件信息 - 大小: ${fileSize} bytes, 修改时间: ${lastModified || '未知'}, 文件时间戳: ${fileTime}, 请求开始时间: ${requestStartTime}, 时间差: ${timeDiff}ms, 已等待: ${elapsedSeconds.toFixed(1)}s`);
                 console.log(`ℹ️ [SVG] 上次记录的修改时间: ${lastModifiedTime}, 上次文件大小: ${lastFileSize}`);
                 
                 if (fileSize > 0) {
                   // ⚠️ 关键：记录初始文件状态（第一次检测到的文件可能是旧文件）
                   if (!initialFileDetected) {
                     initialFileDetected = true;
                     initialFileSize = fileSize;
                     initialModifiedTime = modifiedTime;
                     lastFileSize = fileSize;
                     lastModifiedTime = modifiedTime;
                     console.log(`ℹ️ [SVG] 首次检测到文件 - 大小: ${fileSize} bytes, 修改时间: ${lastModified || '未知'}`);
                     console.log(`ℹ️ [SVG] 这可能是旧文件，将等待文件大小或修改时间变化`);
                   }
                   
                   // ⚠️ 关键判断1：文件大小是否发生变化（这是最可靠的指标）
                   const fileSizeChanged = fileSize !== lastFileSize && lastFileSize > 0;
                   
                   // ⚠️ 关键判断2：文件大小是否与初始不同（说明是新文件覆盖了旧文件）
                   const fileSizeDifferentFromInitial = fileSize !== initialFileSize;
                   
                   // ⚠️ 关键判断3：文件修改时间是否更新
                   const modifiedTimeChanged = modifiedTime && lastModifiedTime && modifiedTime > lastModifiedTime;
                   
                   // ⚠️ 关键判断4：文件修改时间是否晚于请求开始时间（说明是新文件）
                   const isNewFile = modifiedTime && modifiedTime > requestStartTime;
                   
                   // ⚠️ 关键判断5：文件大小是否稳定（连续两次检查大小一致）
                   if (fileSize === lastFileSize && lastFileSize > 0) {
                     stableFileSizeCount++;
                   } else {
                     stableFileSizeCount = 0; // 重置计数
                   }
                   
                   console.log(`🔍 [SVG] 文件大小变化: ${fileSizeChanged} (当前: ${fileSize}, 上次: ${lastFileSize}, 初始: ${initialFileSize})`);
                   console.log(`🔍 [SVG] 文件大小与初始不同: ${fileSizeDifferentFromInitial}`);
                   console.log(`🔍 [SVG] 修改时间变化: ${modifiedTimeChanged} (当前: ${modifiedTime}, 上次: ${lastModifiedTime})`);
                   console.log(`🔍 [SVG] 是否为新文件（修改时间 > 请求开始时间）: ${isNewFile}`);
                   console.log(`🔍 [SVG] 文件大小稳定次数: ${stableFileSizeCount}`);
                   
                   // 更新记录
                   lastFileSize = fileSize;
                   lastModifiedTime = modifiedTime;
                   
                   // ⚠️ 关键加载逻辑：
                   // 1. 如果文件大小发生变化且稳定，说明新文件已写入，等待3秒后加载
                   // 2. 如果文件修改时间晚于请求开始时间且大小稳定，说明是新文件，等待3秒后加载
                   // 3. 如果文件大小与初始不同且稳定，说明新文件已覆盖旧文件，等待5秒后加载
                   // 4. 如果等待时间超过25秒，直接加载（确保新文件已生成，即使检测不到变化）
                   const shouldLoad = (fileSizeChanged && stableFileSizeCount >= 2 && elapsedSeconds > 5) ||  // 文件大小变化且稳定，等待超过5秒
                                     (isNewFile && stableFileSizeCount >= 2 && elapsedSeconds > 3) ||  // 新文件且大小稳定，等待超过3秒
                                     (fileSizeDifferentFromInitial && stableFileSizeCount >= 2 && elapsedSeconds > 5) ||  // 文件大小与初始不同且稳定，等待超过5秒
                                     elapsedSeconds > 25;  // 等待超过25秒，直接加载（确保新文件已生成）
                   
                   console.log(`🔍 [SVG] 是否应该加载: ${shouldLoad} (大小变化: ${fileSizeChanged}, 是否为新文件: ${isNewFile}, 大小与初始不同: ${fileSizeDifferentFromInitial}, 大小稳定: ${stableFileSizeCount >= 2}, 等待时间: ${elapsedSeconds.toFixed(1)}s)`);
                   
                   if (shouldLoad) {
                     // ⚠️ 关键：只有在文件大小变化或文件是新文件时才加载
                     // 如果文件是旧文件（修改时间早于请求开始时间）且大小未变化，继续等待
                     if (!isNewFile && !fileSizeChanged && fileSize === initialFileSize && elapsedSeconds < 25) {
                       console.log(`⚠️ [SVG] 文件是旧文件且大小未变化，继续等待新文件生成... (${retryCount}/${maxRetries}, 已等待 ${elapsedSeconds.toFixed(1)}s)`);
                       if (retryCount < maxRetries) {
                         setTimeout(tryLoadSVG, retryInterval);
                       }
                       return;
                     }
                     
                     console.log(`✅ [SVG] 准备加载 SVG 文件 (大小: ${fileSize} bytes, 修改时间: ${lastModified || '未知'}, 是否为新文件: ${isNewFile}, 大小变化: ${fileSizeChanged}, 已等待 ${elapsedSeconds.toFixed(1)}s)`);
                     
                     // 稍微延迟一下，确保文件完全写入
                     setTimeout(() => {
                       try {
                         // 使用带时间戳和随机数的 URL 加载，避免缓存
                         const loadUrl = svgPath + "?t=" + Date.now() + "&v=" + Math.random();
                         console.log(`🔄 [SVG] 开始加载 SVG: ${loadUrl}`);
                         
                         // 调用显示函数（不抛出错误，让函数内部处理）
                         displayTextOnCanvas(loadUrl);
                         
                         // 标记为成功（即使有部分元素解析错误，只要主要部分加载成功即可）
                         loadSuccess = true;
                         console.log("✅ [SVG] SVG 加载并显示成功（即使有部分元素解析错误，主要部分已显示）");
                       } catch (error) {
                         console.error(`❌ [SVG] SVG 加载失败:`, error);
                         console.error(`❌ [SVG] 错误堆栈:`, error.stack);
                         // 即使加载失败，也继续重试
                         lastModifiedTime = null; // 重置，允许重新检测
                         lastFileSize = 0; // 重置
                         initialFileDetected = false; // 重置初始文件检测标志
                         stableFileSizeCount = 0; // 重置
                         loadSuccess = false; // 重置成功标志
                         if (retryCount < maxRetries) {
                           setTimeout(tryLoadSVG, retryInterval);
                         } else {
                           console.error("❌ [SVG] SVG 加载失败，已达到最大重试次数");
                         }
                       }
                     }, 1000); // 延迟 1秒 确保文件完全写入
                   } else {
                     // 文件存在但还未到加载时机，继续等待
                     console.log(`ℹ️ [SVG] 文件存在但等待更长时间以确保是新文件... (${retryCount}/${maxRetries}, 已等待 ${elapsedSeconds.toFixed(1)}s)`);
                     if (retryCount < maxRetries) {
                       setTimeout(tryLoadSVG, retryInterval);
                     }
                   }
                 } else {
                   console.log(`ℹ️ [SVG] SVG 文件存在但大小为 0，可能还在生成中... (${retryCount}/${maxRetries})`);
                   if (retryCount < maxRetries) {
                     setTimeout(tryLoadSVG, retryInterval);
                   } else {
                     console.error("❌ [SVG] SVG 文件大小为 0，已达到最大重试次数");
                   }
                 }
               } else if (response.status === 404) {
                 // 文件不存在，继续等待
                 console.log(`ℹ️ [SVG] SVG 文件尚未生成 (404), 等待中... (${retryCount}/${maxRetries}, ${elapsedTime}s)`);
                 if (retryCount < maxRetries) {
                   setTimeout(tryLoadSVG, retryInterval);
                 } else {
                   console.error("❌ [SVG] SVG 文件加载超时，已达到最大重试次数");
                 }
               } else {
                 console.warn(`⚠️ [SVG] SVG 文件检查失败 (${response.status}), 继续重试... (${retryCount}/${maxRetries})`);
                 console.warn(`⚠️ [SVG] 响应头:`, Object.fromEntries(response.headers.entries()));
                 if (retryCount < maxRetries) {
                   setTimeout(tryLoadSVG, retryInterval);
                 } else {
                   console.error("❌ [SVG] SVG 文件检查失败，已达到最大重试次数");
                 }
               }
             })
             .catch(error => {
               console.error(`❌ [SVG] 检查 SVG 文件失败 (${retryCount}/${maxRetries}):`, error);
               console.error(`❌ [SVG] 错误详情:`, error.message);
               if (retryCount < maxRetries) {
                 setTimeout(tryLoadSVG, retryInterval);
               } else {
                 console.error("❌ [SVG] SVG 文件检查失败，已达到最大重试次数");
               }
             });
         }
         
         // 延迟一下再开始检查，给后台转换一些时间
         console.log("ℹ️ [SVG] 等待 3 秒后开始检查新生成的 SVG 文件（通过文件大小变化检测新文件）...");
         setTimeout(tryLoadSVG, 3000);
        } else {
          console.warn("⚠️ [SVG] No SVG content or path returned from backend.");
          console.warn("⚠️ [SVG] Available data keys:", Object.keys(data || {}));
        }
      });
    });
}

function addSelectionTrigger() {
  addSelection.value = true;
  select_boxes.value.push(current_box.value);
}

// ✅ 从 SVG 字符串加载（推荐，用于远程服务器）
function displayTextOnCanvasFromString(svgContent) {
  console.log("🔄 [SVG] Loading SVG from string content");
  console.log("🔄 [SVG] SVG content type:", typeof svgContent);
  console.log("🔄 [SVG] SVG content length:", svgContent?.length);
  
  if (!svgContent || svgContent.trim().length === 0) {
    console.error("❌ [SVG] Empty SVG content");
    return;
  }
  
  // 检查 canvas 对象是否存在
  if (!canvas || !canvas.c) {
    console.error("❌ [SVG] Canvas object not found");
    console.error("❌ [SVG] canvas:", canvas);
    return;
  }
  
  console.log("🔄 [SVG] Canvas found, width:", canvas.c.getWidth(), "height:", canvas.c.getHeight());
  
  fabric.loadSVGFromString(svgContent, function (objects, options) {
    // 检查是否成功加载
    if (!objects || objects.length === 0) {
      console.warn("⚠️ [SVG] SVG loaded but no objects found");
      console.warn("⚠️ [SVG] objects:", objects);
      console.warn("⚠️ [SVG] options:", options);
      return;
    }
    
    console.log("✅ [SVG] SVG loaded successfully from string, objects count:", objects.length);
    console.log("✅ [SVG] SVG options:", options);
    
    try {
      const svgObject = fabric.util.groupSVGElements(objects, options);
      svgObject.id = "word";
      
      console.log("✅ [SVG] SVG object created, width:", svgObject.width, "height:", svgObject.height);

      // 删除旧的 word 图层
      const oldObjs = canvas.c.getObjects();
      const oldWordObjs = oldObjs.filter(o => o.id === "word");
      console.log("🗑️ [SVG] Removing old word objects, count:", oldWordObjs.length);
      oldWordObjs.forEach(o => {
        canvas.c.remove(o);
      });

      // 自适应居中
      const cw = canvas.c.getWidth();
      const ch = canvas.c.getHeight();
      console.log("🔄 [SVG] Canvas dimensions:", cw, "x", ch);
      console.log("🔄 [SVG] SVG object dimensions:", svgObject.width, "x", svgObject.height);
      
      if (svgObject.width && svgObject.height) {
        const scale = 0.7 * Math.min(cw / svgObject.width, ch / svgObject.height);
        console.log("🔄 [SVG] Calculated scale:", scale);
        svgObject.scale(scale);
        svgObject.left = (cw - svgObject.width * scale) / 2;
        svgObject.top = (ch - svgObject.height * scale) / 2;
        console.log("🔄 [SVG] SVG position:", svgObject.left, svgObject.top);
      } else {
        console.warn("⚠️ [SVG] SVG object has no width/height, using default scale");
        svgObject.scale(0.7);
        svgObject.left = cw / 2;
        svgObject.top = ch / 2;
      }

      canvas.c.add(svgObject);
      canvas.c.renderAll();
      console.log("✅ [SVG] SVG added to canvas and rendered successfully");
      console.log("✅ [SVG] Canvas objects count:", canvas.c.getObjects().length);
    } catch (error) {
      console.error("❌ [SVG] Error processing SVG objects:", error);
      console.error("❌ [SVG] Error stack:", error.stack);
    }
  }, function(error) {
    console.error("❌ [SVG] Error loading SVG from string:", error);
    console.error("❌ [SVG] Error details:", error);
  });
}

// ✅ 从 URL 路径加载（备用方案）
function displayTextOnCanvas(svgPath = '/src/assets/canvas/word.svg' + "?t=" + Date.now()) {
  console.log("🔄 [SVG] Loading SVG from path:", svgPath);
  
  // 检查 canvas 对象是否存在
  if (!canvas || !canvas.c) {
    console.error("❌ [SVG] Canvas object not found");
    console.error("❌ [SVG] canvas:", canvas);
    throw new Error("Canvas object not found");
  }
  
  console.log("🔄 [SVG] Canvas found, width:", canvas.c.getWidth(), "height:", canvas.c.getHeight());
  
  // 使用更宽松的解析选项，忽略解析错误
  const parseOptions = {
    crossOrigin: 'anonymous',
    // 忽略某些解析错误，继续加载其他元素
    suppressPreamble: true
  };
  
  fabric.loadSVGFromURL(svgPath, function (objects, options) {
    // 检查是否成功加载
    if (!objects || objects.length === 0) {
      console.warn("⚠️ [SVG] SVG loaded but no objects found");
      console.warn("⚠️ [SVG] objects:", objects);
      console.warn("⚠️ [SVG] options:", options);
      // 不抛出错误，而是尝试其他方法
      console.warn("⚠️ [SVG] 尝试使用备用方法加载 SVG");
      return;
    }
    
    console.log("✅ [SVG] SVG loaded successfully, objects count:", objects.length);
    console.log("✅ [SVG] SVG options:", options);
    
    try {
      // 过滤掉无效的对象（如果有的话）
      const validObjects = objects.filter(obj => obj != null);
      if (validObjects.length === 0) {
        console.warn("⚠️ [SVG] 所有对象都无效");
        return;
      }
      
      console.log(`✅ [SVG] 有效对象数量: ${validObjects.length}/${objects.length}`);
      
      // 使用有效的对象创建 SVG 对象
      const svgObject = fabric.util.groupSVGElements(validObjects, options);
      svgObject.id = "word";
      
      console.log("✅ [SVG] SVG object created, width:", svgObject.width, "height:", svgObject.height);

      // 删除旧的 word 图层
      const oldObjs = canvas.c.getObjects();
      const oldWordObjs = oldObjs.filter(o => o.id === "word");
      console.log("🗑️ [SVG] Removing old word objects, count:", oldWordObjs.length);
      oldWordObjs.forEach(o => {
        canvas.c.remove(o);
      });

      // 自适应居中
      const cw = canvas.c.getWidth();
      const ch = canvas.c.getHeight();
      console.log("🔄 [SVG] Canvas dimensions:", cw, "x", ch);
      console.log("🔄 [SVG] SVG object dimensions:", svgObject.width, "x", svgObject.height);
      
      if (svgObject.width && svgObject.height) {
        const scale = 0.7 * Math.min(cw / svgObject.width, ch / svgObject.height);
        console.log("🔄 [SVG] Calculated scale:", scale);
        svgObject.scale(scale);
        svgObject.left = (cw - svgObject.width * scale) / 2;
        svgObject.top = (ch - svgObject.height * scale) / 2;
        console.log("🔄 [SVG] SVG position:", svgObject.left, svgObject.top);
      } else {
        console.warn("⚠️ [SVG] SVG object has no width/height, using default scale");
        svgObject.scale(0.7);
        svgObject.left = cw / 2;
        svgObject.top = ch / 2;
      }

      canvas.c.add(svgObject);
      canvas.c.renderAll();
      console.log("✅ [SVG] SVG added to canvas and rendered successfully");
      console.log("✅ [SVG] Canvas objects count:", canvas.c.getObjects().length);
      
      // 验证 SVG 是否真的显示在画布上
      const addedObjects = canvas.c.getObjects().filter(o => o.id === "word" || o.id?.startsWith("word-"));
      if (addedObjects.length > 0) {
        console.log(`✅ [SVG] 确认 SVG 已添加到画布，对象数量: ${addedObjects.length}`);
        const firstObj = addedObjects[0];
        console.log(`✅ [SVG] SVG 对象位置: left=${firstObj.left}, top=${firstObj.top}, scale=${firstObj.scaleX || firstObj.scale || 'N/A'}`);
        console.log(`✅ [SVG] SVG 对象尺寸: width=${firstObj.width}, height=${firstObj.height}`);
      } else {
        console.warn("⚠️ [SVG] SVG 对象未找到，可能未正确添加");
      }
    } catch (error) {
      console.error("❌ [SVG] Error processing SVG objects:", error);
      console.error("❌ [SVG] Error stack:", error.stack);
      // 不抛出错误，而是尝试直接添加对象
      console.warn("⚠️ [SVG] 尝试直接添加对象到画布");
      try {
        // 删除旧的 word 图层
        const oldObjs = canvas.c.getObjects();
        const oldWordObjs = oldObjs.filter(o => o.id === "word");
        oldWordObjs.forEach(o => canvas.c.remove(o));
        
        // 直接添加所有有效对象
        const validObjects = objects.filter(obj => obj != null);
        if (validObjects.length > 0) {
          // 计算整体边界框，用于居中
          let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
          validObjects.forEach(obj => {
            if (obj.left !== undefined && obj.top !== undefined) {
              const objWidth = obj.width * (obj.scaleX || 1);
              const objHeight = obj.height * (obj.scaleY || 1);
              minX = Math.min(minX, obj.left);
              minY = Math.min(minY, obj.top);
              maxX = Math.max(maxX, obj.left + objWidth);
              maxY = Math.max(maxY, obj.top + objHeight);
            }
          });
          
          const cw = canvas.c.getWidth();
          const ch = canvas.c.getHeight();
          const groupWidth = maxX - minX;
          const groupHeight = maxY - minY;
          
          // 计算居中偏移
          const offsetX = (cw - groupWidth) / 2 - minX;
          const offsetY = (ch - groupHeight) / 2 - minY;
          
          validObjects.forEach((obj, index) => {
            obj.id = `word-${index}`;
            // 调整位置以居中
            if (obj.left !== undefined) obj.left += offsetX;
            if (obj.top !== undefined) obj.top += offsetY;
            canvas.c.add(obj);
          });
          canvas.c.renderAll();
          console.log("✅ [SVG] 直接添加对象成功，对象数量:", validObjects.length);
          console.log(`✅ [SVG] 对象已居中，偏移: x=${offsetX.toFixed(2)}, y=${offsetY.toFixed(2)}`);
        } else {
          console.warn("⚠️ [SVG] 没有有效的对象可以添加");
        }
      } catch (fallbackError) {
        console.error("❌ [SVG] 备用方法也失败:", fallbackError);
      }
    }
  }, function(error) {
    // 错误回调：某些元素解析失败，但不影响整体加载
    // 注意：fabric.js 在解析某些元素时可能会调用错误回调，但成功回调可能仍然会被调用
    console.warn("⚠️ [SVG] 某些 SVG 元素解析失败（这是正常的，fabric.js 会继续加载其他元素）:", error);
    // 不抛出错误，让成功回调处理
  }, parseOptions);
}


// =================== ABOUT IDEA ===========================
let ttipContent1 = ref("explanation")
let ttipContent2 = ref("explanation")
let ttipContent3 = ref("explanation")
let ttipContent4 = ref("explanation")
let ttipContent5 = ref("explanation")
function clickBrainstorm() {
  const textareaIdea = document.getElementById("idea");
  console.log("press storm")
  let param = {
    "user_prompt": textareaIdea.value
  };

  startBrainStorm(param, function (data) {
    var count = 1

    for (let key in data) {
      let concept = key;
      let explanation = data[key];
      const labelConcept = document.getElementById("tag-concept" + String(count)); const tooltipConcept = document.getElementById("item-concept" + String(count));
      labelConcept.textContent = concept;
      if (count == 1) {
        ttipContent1.value = explanation
      }
      if (count == 2) {
        ttipContent2.value = explanation
      }
      if (count == 3) {
        ttipContent3.value = explanation
      }
      if (count == 4) {
        ttipContent4.value = explanation
      }
      if (count == 5) {
        ttipContent5.value = explanation
      }
      count++;
    }
  });
}

// =================== ABOUT IMAGE ==========================
let isExistCanvasImage = ref(false)
let firstDisplay = ref(true)

// anchor 锚点，抛锚
function loadImageOrDisplay1() {
  var img1 = document.getElementById("img1");
  // 初始上传，点击上传本地文件
  if (img1.src.includes("default1.png")) {
    document.getElementById('input-img1').click()
    document.getElementById('input-img1').addEventListener('change', function (event) {
      var file = event.target.files[0];
      var reader = new FileReader();
      reader.onload = function (event) {
        img1.src = event.target.result;
      };
      reader.readAsDataURL(file);
    });
  }
  // 已经上传好了，点击显示到canvas上
  else {
    // 删掉原有的canvas再新建一个，再加入fabric canvas
    // fabric canvas 有两个，原先的这个canvas只是第一个，共同归属canvas-container管
    var oldCanvas = document.getElementById("canva-img");
    if (firstDisplay.value) {
      oldCanvas.parentNode.removeChild(oldCanvas);
      firstDisplay.value = false
    }
    else {
      var parentElement = oldCanvas.parentNode;
      var grandparentElement = parentElement.parentNode;
      grandparentElement.removeChild(parentElement);
    }

    // add new canvas
    const imgInputDiv = document.querySelector(".img-input");
    const canvasImage0 = document.createElement("canvas")

    canvasImage0.id = "canva-img";
    canvasImage0.width = 180;
    canvasImage0.height = 180;
    imgInputDiv.appendChild(canvasImage0);

    // add style for canvas
    const style = document.createElement("style");
    style.innerHTML = `
    .canvas-container {
      background-color: #ffffff;
      padding: 5px 8px;
      border-radius: 6px;
      border: 1px solid #D8D2B3; }`;
    document.head.appendChild(style);

    // add image instance 
    const canvasImage = new fabric.Canvas('canva-img');
    canvasImage.setWidth(180);
    canvasImage.setHeight(180);
    canvasImage.renderAll()

    const imgInstance = new fabric.Image(img1, {
      left: 15, top: 10,
    });

    imgInstance.scaleToWidth(canvasImage.getWidth());
    imgInstance.scaleToHeight(canvasImage.getHeight());

    canvasImage.add(imgInstance);
    imgInstance.selectable = false; // image is not movable

    // canvasImage.renderAll()
    isExistCanvasImage.value = !isExistCanvasImage.value

    // free draw rectangle
    var origX, origY;
    let inputPoints = [];

    canvasImage.on('mouse:down', function (o) {
      var pointer = canvasImage.getPointer(o.e);

      origX = pointer.x;
      origY = pointer.y;
      inputPoints.push([origX - 15, origY - 10])

      const anchorImg = document.createElement('img');
      anchorImg.src = "src/assets/upload_image/anchor.png"
      // 插入页面
      document.body.appendChild(anchorImg);
      anchorImg.onload = () => { // 必须要加onload，等图片加载完全，不然就是空的
        // canvasImage.clear();
        const anchorInstance = new fabric.Image(anchorImg, {
          left: origX - 15,
          top: origY - 10,
        });

        // anchorInstance.scaleToWidth(canvasImage.getWidth());
        // anchorInstance.scaleToHeight(canvasImage.getHeight());
        canvasImage.add(anchorInstance);
        anchorInstance.selectable = false; // image is not movable
        // canvasImage.renderAll()
        anchorImg.remove()
      }
    });

    // 这个就是信号
    canvasImage.on('mouse:up', function (o) {
      let param = {
        // XYXY format
        "points": inputPoints,
        "image_url": img1.src,
        "mode": "image"
      };

      imageSegment(param, function (data) {
        console.log("✅ [IMAGE Mode] Received data from backend:", data);
        const imgEl = document.createElement('img');
        // 确保使用后端返回的 base64 数据，不添加查询参数（base64 data URL 不需要）
        const imageDataUrl = data.highlight || data;
        if (!imageDataUrl) {
          console.error("❌ No image data received from backend");
          return;
        }
        imgEl.src = imageDataUrl;  // base64 data URL 不需要添加时间戳参数
        // 插入页面
        document.body.appendChild(imgEl);
        imgEl.onload = () => { // 必须要加onload，等图片加载完全，不然就是空的
          canvasImage.clear();
          const imgInstanceNew = new fabric.Image(imgEl, {
            left: 15, top: 10,
          });
          // 设置缩放
          imgInstanceNew.scaleToWidth(canvasImage.getWidth());
          imgInstanceNew.scaleToHeight(canvasImage.getHeight());
          imgInstanceNew.selectable = false;

          canvasImage.add(imgInstanceNew)
          canvasImage.renderAll()
          // 删除页面中的图片元素
          imgEl.remove()
        }
        canvasImage.renderAll()
      })
    });

  };
}
function loadImageOrDisplay2() {
  var img2 = document.getElementById("img2");
  // 初始上传，点击上传本地文件
  if (img2.src.includes("default1.png")) {
    document.getElementById('input-img2').click()
    document.getElementById('input-img2').addEventListener('change', function (event) {
      var file = event.target.files[0];
      var reader = new FileReader();
      reader.onload = function (event) {
        img2.src = event.target.result;
      };
      reader.readAsDataURL(file);
    });
  }
  // 已经上传好了，点击显示到canvas上
  else {
    // 删掉原有的canvas再新建一个，再加入fabric canvas
    // fabric canvas 有两个，原先的这个canvas只是第一个，共同归属canvas-container管
    var oldCanvas = document.getElementById("canva-img");
    if (firstDisplay.value) {
      oldCanvas.parentNode.removeChild(oldCanvas);
      firstDisplay.value = false
    }
    else {
      var parentElement = oldCanvas.parentNode;
      var grandparentElement = parentElement.parentNode;
      grandparentElement.removeChild(parentElement);
    }

    // add new canvas
    const imgInputDiv = document.querySelector(".img-input");
    const canvasImage0 = document.createElement("canvas")

    canvasImage0.id = "canva-img";
    canvasImage0.width = 180;
    canvasImage0.height = 180;
    imgInputDiv.appendChild(canvasImage0);

    // add style for canvas
    const style = document.createElement("style");
    style.innerHTML = `
    .canvas-container {
      background-color: #ffffff;
      padding: 5px 8px;
      border-radius: 6px;
      border: 1px solid #D8D2B3; }`;
    document.head.appendChild(style);

    // add image instance 
    const canvasImage = new fabric.Canvas('canva-img');
    canvasImage.setWidth(180);
    canvasImage.setHeight(180);
    canvasImage.renderAll()

    const imgInstance = new fabric.Image(img2, {
      left: 15, top: 10,
    });

    imgInstance.scaleToWidth(canvasImage.getWidth());
    imgInstance.scaleToHeight(canvasImage.getHeight());

    canvasImage.add(imgInstance);
    imgInstance.selectable = false; // image is not movable

    // canvasImage.renderAll()
    isExistCanvasImage.value = !isExistCanvasImage.value

    // free draw rectangle
    var origX, origY;
    let inputPoints = [];

    canvasImage.on('mouse:down', function (o) {
      var pointer = canvasImage.getPointer(o.e);

      origX = pointer.x;
      origY = pointer.y;
      inputPoints.push([origX - 15, origY - 10])

      const anchorImg = document.createElement('img');
      anchorImg.src = "src/assets/upload_image/anchor.png"
      // 插入页面
      document.body.appendChild(anchorImg);
      anchorImg.onload = () => { // 必须要加onload，等图片加载完全，不然就是空的
        // canvasImage.clear();
        const anchorInstance = new fabric.Image(anchorImg, {
          left: origX - 15,
          top: origY - 10,
        });

        // anchorInstance.scaleToWidth(canvasImage.getWidth());
        // anchorInstance.scaleToHeight(canvasImage.getHeight());
        canvasImage.add(anchorInstance);
        anchorInstance.selectable = false; // image is not movable
        // canvasImage.renderAll()
        anchorImg.remove()
      }
    });

    // 这个就是信号
    canvasImage.on('mouse:up', function (o) {
      let param = {
        // XYXY format
        "points": inputPoints,
        "image_url": img2.src,
        "mode": "image"
      };

      imageSegment(param, function (data) {
        console.log("✅ [IMAGE Mode] Received data from backend:", data);
        const imgEl = document.createElement('img');
        // 确保使用后端返回的 base64 数据，不添加查询参数（base64 data URL 不需要）
        const imageDataUrl = data.highlight || data;
        if (!imageDataUrl) {
          console.error("❌ No image data received from backend");
          return;
        }
        imgEl.src = imageDataUrl;  // base64 data URL 不需要添加时间戳参数
        // 插入页面
        document.body.appendChild(imgEl);
        imgEl.onload = () => { // 必须要加onload，等图片加载完全，不然就是空的
          canvasImage.clear();
          const imgInstanceNew = new fabric.Image(imgEl, {
            left: 15, top: 10,
          });
          // 设置缩放
          imgInstanceNew.scaleToWidth(canvasImage.getWidth());
          imgInstanceNew.scaleToHeight(canvasImage.getHeight());
          imgInstanceNew.selectable = false;

          canvasImage.add(imgInstanceNew)
          canvasImage.renderAll()
          // 删除页面中的图片元素
          imgEl.remove()
        }
        canvasImage.renderAll()
      })
    });

  };
}
function loadImageOrDisplay3() {
  var img3 = document.getElementById("img3");
  // 初始上传，点击上传本地文件
  if (img3.src.includes("default1.png")) {
    document.getElementById('input-img3').click()
    document.getElementById('input-img3').addEventListener('change', function (event) {
      var file = event.target.files[0];
      var reader = new FileReader();
      reader.onload = function (event) {
        img3.src = event.target.result;
      };
      reader.readAsDataURL(file);
    });
  }
  // 已经上传好了，点击显示到canvas上
  else {
    // 删掉原有的canvas再新建一个，再加入fabric canvas
    // fabric canvas 有两个，原先的这个canvas只是第一个，共同归属canvas-container管
    var oldCanvas = document.getElementById("canva-img");
    if (firstDisplay.value) {
      oldCanvas.parentNode.removeChild(oldCanvas);
      firstDisplay.value = false
    }
    else {
      var parentElement = oldCanvas.parentNode;
      var grandparentElement = parentElement.parentNode;
      grandparentElement.removeChild(parentElement);
    }

    // add new canvas
    const imgInputDiv = document.querySelector(".img-input");
    const canvasImage0 = document.createElement("canvas")

    canvasImage0.id = "canva-img";
    canvasImage0.width = 180;
    canvasImage0.height = 180;
    imgInputDiv.appendChild(canvasImage0);

    // add style for canvas
    const style = document.createElement("style");
    style.innerHTML = `
    .canvas-container {
      background-color: #ffffff;
      padding: 5px 8px;
      border-radius: 6px;
      border: 1px solid #D8D2B3; }`;
    document.head.appendChild(style);

    // add image instance 
    const canvasImage = new fabric.Canvas('canva-img');
    canvasImage.setWidth(180);
    canvasImage.setHeight(180);
    canvasImage.renderAll()

    const imgInstance = new fabric.Image(img3, {
      left: 15, top: 10,
    });

    imgInstance.scaleToWidth(canvasImage.getWidth());
    imgInstance.scaleToHeight(canvasImage.getHeight());

    canvasImage.add(imgInstance);
    imgInstance.selectable = false; // image is not movable

    // canvasImage.renderAll()
    isExistCanvasImage.value = !isExistCanvasImage.value

    // free draw rectangle
    var origX, origY;
    let inputPoints = [];

    canvasImage.on('mouse:down', function (o) {
      var pointer = canvasImage.getPointer(o.e);

      origX = pointer.x;
      origY = pointer.y;
      inputPoints.push([origX - 15, origY - 10])

      const anchorImg = document.createElement('img');
      anchorImg.src = "src/assets/upload_image/anchor.png"
      // 插入页面
      document.body.appendChild(anchorImg);
      anchorImg.onload = () => { // 必须要加onload，等图片加载完全，不然就是空的
        // canvasImage.clear();
        const anchorInstance = new fabric.Image(anchorImg, {
          left: origX - 15,
          top: origY - 10,
        });

        // anchorInstance.scaleToWidth(canvasImage.getWidth());
        // anchorInstance.scaleToHeight(canvasImage.getHeight());
        canvasImage.add(anchorInstance);
        anchorInstance.selectable = false; // image is not movable
        // canvasImage.renderAll()
        anchorImg.remove()
      }
    });

    // 这个就是信号
    canvasImage.on('mouse:up', function (o) {
      let param = {
        // XYXY format
        "points": inputPoints,
        "image_url": img3.src,
        "mode": "image"
      };

      imageSegment(param, function (data) {
        console.log("✅ [IMAGE Mode] Received data from backend:", data);
        const imgEl = document.createElement('img');
        // 确保使用后端返回的 base64 数据，不添加查询参数（base64 data URL 不需要）
        const imageDataUrl = data.highlight || data;
        if (!imageDataUrl) {
          console.error("❌ No image data received from backend");
          return;
        }
        imgEl.src = imageDataUrl;  // base64 data URL 不需要添加时间戳参数
        // 插入页面
        document.body.appendChild(imgEl);
        imgEl.onload = () => { // 必须要加onload，等图片加载完全，不然就是空的
          canvasImage.clear();
          const imgInstanceNew = new fabric.Image(imgEl, {
            left: 15, top: 10,
          });
          // 设置缩放
          imgInstanceNew.scaleToWidth(canvasImage.getWidth());
          imgInstanceNew.scaleToHeight(canvasImage.getHeight());
          imgInstanceNew.selectable = false;

          canvasImage.add(imgInstanceNew)
          canvasImage.renderAll()
          // 删除页面中的图片元素
          imgEl.remove()
        }
        canvasImage.renderAll()
      })
    });

  };
}


function startExtract() {
  let param = "123"
  startImageExtract(param, function (data) {
    storeDesignPrior.semanticImage = data.semantic,
      storeDesignPrior.colorImage = data.color,
      storeDesignPrior.shapeImage = data.shape,
      storeDesignPrior.shapePrompt = data.semantic_prompt,
      // storeDesignPrior.svgString = data.svg_string,
      storeDesignPrior.sampledPoints = data.sampled_points,
      eventBus.emit("isExtract", {
        "message": "show design prior in Generate view",
      })
  })
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
:deep(.ivu-tooltip-inner) {
  white-space: normal;
}

:deep(.ivu-tooltip) {
  display: block;
}

:deep(.ivu-tooltip-rel) {
  display: block;
}

// .wordView {
//   width: 100%;
//   height: 33%;
//   margin-top: -41px;
//   background: #fff;
//   position: relative;
//   z-index: 1;
//   vertical-align: auto;
// }

// .ideaView {
//   width: 100%;
//   height: 22%;
//   margin-top: -25px;
//   background: #fff;
// }

.wordView {
  width: 100%;
  height: 33%;
  margin-top: -25px;
  background: #fff;
  position: relative;
  z-index: 1;
  vertical-align: auto;
}

.ideaView {
  width: 100%;
  height: 22%;
  margin-top: -41px;
  background: #fff;
}

.imageView {
  width: 100%;
  height: 29%;
  margin-top: -25px;
  background: #fff;
}

h3 {
  margin-top: 30px;
  text-align: left;
  text-transform: uppercase;
  background: #fff;
  padding-top: 5px;
  padding-left: 10px;

  font-family: "DM Sans", sans-serif;
  color: #2a2a2a;
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 10px;
}

.text-word {
  // margin-top: 10px;
  // margin-left: 2px;
  width: 90%;
  height: 22px;
  -moz-border-bottom-colors: none;
  -moz-border-left-colors: none;
  -moz-border-right-colors: none;
  -moz-border-top-colors: none;
  background: none repeat scroll 0 0 #F7F6F0;
  border-color: -moz-use-text-color #FFFFFF #FFFFFF -moz-use-text-color;
  border-image: none;
  border-radius: 6px 6px 6px 6px;
  // border-style: none solid solid none;
  border-style: none;
  // border-width: medium 1px 1px medium;
  // box-shadow: 0 1px 2px rgba(99, 99, 99, 0.12) inset;
  color: #4f4f4f;
  font-family: "DM Sans", sans-serif;
  font-size: 14px;
  line-height: 1.4em;
  padding: 5px 8px;
  transition: background-color 0.2s ease 0s;
}

.text-word:focus {
  background: none repeat scroll 0 0 #f9f9f9;
  outline-width: 0;
}

.text-idea {
  // margin-top: 10px;
  // margin-left: 2px;
  width: 89%;
  height: 44px;
  -moz-border-bottom-colors: none;
  -moz-border-left-colors: none;
  -moz-border-right-colors: none;
  -moz-border-top-colors: none;
  background: none repeat scroll 0 0 #F7F6F0;
  border-color: -moz-use-text-color #FFFFFF #FFFFFF -moz-use-text-color;
  border-image: none;
  border-radius: 6px 6px 6px 6px;
  // border-style: none solid solid none;
  border-style: none;
  // border-width: medium 1px 1px medium;
  // box-shadow: 0 1px 2px rgba(99, 99, 99, 0.12) inset;
  color: #4f4f4f;
  font-family: "DM Sans", sans-serif;
  font-size: 14px;
  line-height: 1.4em;
  padding: 5px 8px;
  transition: background-color 0.2s ease 0s;
}

.text-idea:focus {
  background: none repeat scroll 0 0 #f9f9f9;
  outline-width: 0;
}

.button-idea {
  // display: inline-block;
  // padding-left: 5px;
  margin-right: 11px;
  background-color: #EDEFAB;
  width: 68px;
  height: 52px;
  border-radius: 4px;
  text-align: center;
  /* 将文本水平居中 */
  font-size: 13px;
  color: #797B0B;
  /* 设置字体大小为10px */
  line-height: 13px;
}

.tags {
  list-style: none;
  margin: 0;
  overflow: hidden;
  padding: 0;
  font-size: 13px;
  margin-top: 5px;
}

.tags li {
  float: left;
}

.tag {
  background: #F7F6F0;
  border-radius: 3px 0 0 3px;
  color: #797B0B;
  display: inline-block;
  height: 20px;
  line-height: 20px;
  padding: 0 15px 0 8px;
  position: relative;
  margin: 0 10px 5px 0;
  text-decoration: none;
  // -webkit-transition: color 0.2s;
}

// .tag::before {
//   background: #fff;
//   border-radius: 10px;
//   box-shadow: inset 0 1px rgba(0, 0, 0, 0.25);
//   content: '';
//   height: 6px;
//   left: 10px;
//   position: absolute;
//   width: 6px;
//   top: 10px;
// }

.tag::after {
  background: #fff;
  border-bottom: 10px solid transparent;
  border-left: 9px solid #F7F6F0;
  border-top: 11px solid transparent;
  content: '';
  position: absolute;
  right: 0;
  top: 0;
}

.tag:hover {
  background-color: #EDEFAB;
  // color: white;
  color: #797B0B;
}

.tooltip {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 8px;
  border-radius: 4px;
}

.tag:hover::after {
  border-left-color: #EDEFAB;
  color: #797B0B;
}

.upload-img {
  padding: 0px;
  margin-left: -10px;
  margin-right: 5px;
  margin-bottom: 6px;
  width: 50px;
  height: 50px;
  border-radius: 10px;
}

.upload-img img {
  border-radius: 6px;
}

input[type="file"] {
  display: none;
}

.lassoButton-img {
  // display: inline-block;
  background-color: #EDEFAB;
  margin-left: -10px;
  // padding-left: 7px;
  // margin-right: 11px;
  width: 50px;
  height: 22px;
  border-radius: 4px;
  text-align: center;
  font-size: 13px;
  color: #797B0B;
  /* 设置字体大小为10px */
  line-height: 2px;
  /* 设置行高等于按钮的高度，以实现垂直居中 */
}

.lassoButton-img>.icon-function-small path {
  fill: #797B0B;
}

.icon-function-small {
  margin-top: -5px;
  width: 14px;
  height: 14px
}

.canva-word-container {
  width: 89%;
}

canvas {
  // canvas的长宽不要通过css来设，直接在html申明
  background-color: #ffffff;
  padding: 5px 8px;
  border-radius: 6px;
  border: 1px solid #d8d2b3;
}

.word-options {
  display: flex;
  align-items: center;
  /* 将按钮容器中的内容垂直居中 */
  margin-bottom: 5px;
}

.inline-button {
  display: inline-block;
  margin-right: 5px;
  // /* 可调整按钮之间的间距 */ F5F5F5
  background-color: #EDEFAB;
  width: 60px;
  height: 24px;
  border-radius: 4px;
  text-align: center;
  /* 将文本水平居中 */
  font-size: 13px;
  color: #797B0B;
  /* 设置字体大小为10px */
  line-height: 3px;
  /* 设置行高等于按钮的高度，以实现垂直居中 */
}

.inline-button>.icon-function path {
  fill: #797B0B;
}

.icon-function {
  margin-top: -5px;
  width: 16px;
  height: 16px
}

.title-btn {
  background-color: #EDEFAB;
  border: none;
  border-radius: 5px;
  color: white;
  padding: 4px 4px;
  font-size: 18px;
  margin-right: 5px;
}

/* Darker background on mouse-over */
.title-btn.active {
  background-color: #EEF9FF;
  border: 15px;
  border-color: #a1a1a1;
}

// .btn:focus svg {
//   // color: #465EEA;
//   color: #465EEA;
// }
.title-btn>.icon path {
  fill: #797B0B;
}

.icon {
  width: 20px;
  height: 20px
}


input[type="text"],
select {
  // display: block;
  width: 40%;
  color: #6F6E7E;
  height: 24px;
  padding: 3px;
  padding-left: 12%;
  font-size: 13px;
  border-radius: 5px;
  border: 1.5px solid #E1E4EB;
  margin-bottom: 0px;
  box-sizing: border-box;
}

.button-8 {
  width: 80%;
  height: 23px;
  background-color: #d6eaf4; //e1ecf4
  border-radius: 3px;
  border: 0px solid #EEF9FF; //#7aa7c7
  // box-shadow: rgba(255, 255, 255, .7) 0 1px 0 0 inset;
  box-sizing: border-box;
  color: #39739d;
  cursor: pointer;
  display: flex;
  align-items: center;
  /* 垂直居中 */
  justify-content: center;
  /* 水平居中 */
  font-family: -apple-system, system-ui, "Segoe UI", "Liberation Sans", sans-serif;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.15385;
  margin: 0;
  outline: none;
  // padding: 8px 8px;
  // position: relative;
  // text-align: center;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: baseline;
  white-space: nowrap;
}

.button-8:hover {
  background-color: #b3d3ea;
  color: #2c5777;
}

.button-8:active {
  background-color: #a0c7e4;
  box-shadow: none;
  // color: #2c5777;
}

button {
  background-color: #ccc;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
