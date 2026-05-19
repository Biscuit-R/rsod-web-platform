// router/index.js
import { createRouter, createWebHistory } from "vue-router";
import inference from "../views/Inference.vue"; // Yolo 推理验证页面
import test_connect from "../views/test_connect.vue";

// 路由配置
const routes = [
  {
    path: "/",
    name: "inference",
    component: inference, // 默认打开就是检测页面
  },
  {
    path: "/test-connect",
    name: "test_connect",
    component: test_connect,
  },
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
