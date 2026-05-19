<template>
  <div class="targets-page">
    <div class="page-header">
      <h1 class="page-title">目标检测库</h1>
      <p class="page-subtitle">平台支持检测的所有遥感目标类别</p>
    </div>

    <div class="search-container">
      <el-input v-model="searchQuery" placeholder="搜索目标类别..." size="default" class="search-input">
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon target-icon"><el-icon><Aim /></el-icon></div>
        <div class="stat-info">
          <div class="stat-value">{{ totalTargets }}</div>
          <div class="stat-label">目标总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon category-icon"><el-icon><Grid /></el-icon></div>
        <div class="stat-info">
          <div class="stat-value">{{ categories.length }}</div>
          <div class="stat-label">类别数量</div>
        </div>
      </div>
    </div>

    <div class="target-categories">
      <div v-for="category in filteredCategories" :key="category.id" class="category-card">
        <div class="category-header">
          <div class="category-icon" :style="{ backgroundColor: category.color }">
            <el-icon :size="24" color="white"><component :is="category.icon" /></el-icon>
          </div>
          <div class="category-info">
            <div class="category-name">{{ category.name }}</div>
            <div class="category-count">{{ category.targets.length }} 个目标</div>
          </div>
        </div>
        <div class="target-list">
          <div v-for="target in category.targets" :key="target.id" class="target-item">
            <el-icon :size="14" class="target-item-icon"><CircleCheck /></el-icon>
            <span>{{ target.name }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="filteredCategories.length === 0" class="empty-state">
      <el-icon :size="64" class="empty-icon"><Help /></el-icon>
      <p class="empty-text">未找到匹配的目标类别</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import {
  Search, Aim, Grid, CircleCheck, Help,
  Bicycle, OfficeBuilding, Sunny, Setting,
} from "@element-plus/icons-vue";

const searchQuery = ref("");

const categories = ref([
  {
    id: 1, name: "交通工具类", icon: Bicycle, color: "#3b82f6",
    targets: [
      { id: 1, name: "飞机" }, { id: 2, name: "船舶" }, { id: 3, name: "汽车" },
      { id: 4, name: "火车" }, { id: 5, name: "卡车" },
    ],
  },
  {
    id: 2, name: "建筑设施类", icon: OfficeBuilding, color: "#10b981",
    targets: [
      { id: 6, name: "油罐" }, { id: 7, name: "立交桥" }, { id: 8, name: "体育场" },
      { id: 9, name: "港口" }, { id: 10, name: "机场跑道" },
    ],
  },
  {
    id: 3, name: "自然地貌类", icon: Sunny, color: "#f59e0b",
    targets: [
      { id: 11, name: "湖泊" }, { id: 12, name: "河流" }, { id: 13, name: "森林" },
      { id: 14, name: "农田" }, { id: 15, name: "山地" },
    ],
  },
  {
    id: 4, name: "其他目标", icon: Setting, color: "#8b5cf6",
    targets: [
      { id: 16, name: "风力发电机" }, { id: 17, name: "太阳能板" }, { id: 18, name: "桥梁" },
      { id: 19, name: "烟囱" }, { id: 20, name: "储水池" },
    ],
  },
]);

const filteredCategories = computed(() => {
  if (!searchQuery.value) return categories.value;
  const query = searchQuery.value.toLowerCase();
  return categories.value.map((category) => ({
    ...category,
    targets: category.targets.filter((target) => target.name.toLowerCase().includes(query)),
  })).filter((category) => category.name.toLowerCase().includes(query) || category.targets.length > 0);
});

const totalTargets = computed(() => categories.value.reduce((sum, c) => sum + c.targets.length, 0));
</script>

<style scoped lang="scss">
.targets-page {
  width: 100%;

  .page-header {
    margin-bottom: 24px;
    .page-title { font-size: 24px; font-weight: 600; color: var(--text-primary); margin-bottom: 8px; }
    .page-subtitle { font-size: 14px; color: var(--text-secondary); }
  }

  .search-container { margin-bottom: 24px; .search-input { max-width: 300px; } }

  .stats-cards {
    display: flex; gap: 20px; margin-bottom: 24px;
    .stat-card {
      flex: 1; max-width: 200px; background-color: #ffffff; border-radius: 12px;
      padding: 20px; box-shadow: var(--card-shadow); display: flex; align-items: center; gap: 16px;
      .stat-icon {
        width: 50px; height: 50px; border-radius: 12px; display: flex;
        align-items: center; justify-content: center; color: white; font-size: 24px;
        &.target-icon { background-color: #27ae60; }
        &.category-icon { background-color: #3b82f6; }
      }
      .stat-info {
        .stat-value { font-size: 24px; font-weight: 600; color: var(--text-primary); }
        .stat-label { font-size: 13px; color: var(--text-secondary); }
      }
    }
  }

  .target-categories {
    display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px;
    .category-card {
      background-color: #ffffff; border-radius: 12px; padding: 20px;
      box-shadow: var(--card-shadow); transition: all 0.2s;
      &:hover { box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08); }

      .category-header {
        display: flex; align-items: center; margin-bottom: 16px;
        .category-icon {
          width: 50px; height: 50px; border-radius: 12px; display: flex;
          align-items: center; justify-content: center; margin-right: 16px;
        }
        .category-info {
          .category-name { font-size: 18px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }
          .category-count { font-size: 13px; color: var(--text-secondary); }
        }
      }

      .target-list {
        display: flex; flex-wrap: wrap; gap: 8px;
        .target-item {
          display: flex; align-items: center; gap: 6px; padding: 8px 14px;
          background-color: #f3f4f6; border-radius: 20px; font-size: 14px;
          color: var(--text-secondary); cursor: pointer; transition: all 0.2s;
          &:hover { background-color: rgba(39, 174, 96, 0.1); color: #27ae60; }
          .target-item-icon { color: #27ae60; }
        }
      }
    }
  }

  .empty-state {
    display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 0;
    .empty-icon { color: #9ca3af; margin-bottom: 16px; }
    .empty-text { font-size: 15px; color: var(--text-secondary); }
  }
}
</style>
