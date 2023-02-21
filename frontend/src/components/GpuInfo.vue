<template>
  <a-table
    :columns="columns"
    :data-source="gpu_info_data"
    size="small"
    :pagination="false"
    :style="{ width: 'auto', backgroundColor: 'white', padding: '1rem' }"
  >
    <template #bodyCell="{ column, text }">
      <template v-if="column.dataIndex === 'hostname'">
        <span>{{ text }}</span>
      </template>
      <template v-if="column.dataIndex === 'time'">
        <span>{{ dateFilter(text) }}</span>
      </template>
      <template v-if="column.key === 'index'">
        <span>{{ text }}</span>
      </template>
      <template v-if="column.key === 'process'">
        <span v-for="p in text">{{
          ` ${p["username"]} (${p["gpu_memory_usage"]})`
        }}</span>
      </template>
      <template v-if="column.key === 'pid'">
        <li v-for="p in text">
          {{ p["pid"] }}
        </li>
      </template>
    </template>
  </a-table>
</template>
<script lang="tsx" setup>
import { ref, defineComponent, onMounted, onBeforeUnmount } from "vue";
import dayjs from "dayjs";

const dateFilter = (val: string, format = "YYYY-MM-DD HH:mm:ss") => {
  console.log(val, dayjs(val).format(format))
  return dayjs(val).format(format);
};

const columns = [
  {
    title: "server",
    dataIndex: "hostname",
    key: "hostname",
    align: "center",
  },
  {
    title: "gpu",
    dataIndex: "name",
    key: "gpu",
    align: "center",
  },
  {
    title: "time",
    dataIndex: "time",
    key: "time",
    align: "center",
  },
  {
    title: "index",
    dataIndex: "index",
    key: "index",
    align: "center",
  },
  {
    title: "utilization",
    dataIndex: "utilization.gpu",
    key: "utilization.gpu",
    align: "center",
    customRender: ({ record, index }: { record: any; index: number }) => {
      let color = "black";
      if (record["utilization.gpu"] >= 80) {
        color = "#ff3333";
      } else if (record["utilization.gpu"] >= 60) {
        color = "orange";
      } else {
        color = "#3FBF46";
      }
      return (
        <span style={{ color: color, fontWeight: "bold" }}>
          {record["utilization.gpu"]}%
        </span>
      );
    },
  },
  {
    title: "memory",
    dataIndex: "memory",
    key: "memory",
    align: "center",
    customRender: ({ record, index }: { record: any; index: number }) => {
      let color = "black";
      const val = (record["memory.used"] / record["memory.total"]) * 100;
      if (val >= 80) {
        color = "#ff3333";
      } else if (val >= 60) {
        color = "orange";
      } else {
        color = "#3FBF46";
      }
      return (
        <div>
          <li
            style={{ color: color, fontWeight: "bold" }}
          >{`${record["memory.used"]} / ${record["memory.total"]}`}</li>
        </div>
      );
    },
  },
  {
    title: "processes",
    dataIndex: "processes",
    key: "processes",
    align: "center",
    customRender: ({ record, index }: { record: any; index: number }) => {
      const lists = [];
      for (let i = 0; i < record["processes"].length; ++i) {
        let cpu_percent = record["processes"][i]["cpu_percent"]
        let color = "black"
        if (cpu_percent < 3)
          color = "red";
        lists.push(
          <li style={{ color: color }}>{`${record["processes"][i]["username"]}(${record["processes"][i]["gpu_memory_usage"]})`}</li>
        );
      }
      return <div>{lists}</div>;
    },
  },
  {
    title: "pid",
    dataIndex: "processes",
    key: "pid",
    align: "center",
  },
];
const gpu_info_data = ref(null);
const ws = new WebSocket(`ws://${import.meta.env.VITE_HOST}:${import.meta.env.VITE_BACKEND_PORT}/ws`);

ws.onmessage = (e) => {
  let json = JSON.parse(e.data);
  gpu_info_data.value = json;
};
</script>
<style scoped>
.ant-table {
  table-layout: fixed;
}
</style>
