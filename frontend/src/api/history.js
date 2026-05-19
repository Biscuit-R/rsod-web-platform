import request from '../utils/request'

// 获取检测历史列表
export function getHistoryList(params) {
  return request({
    url: '/history/list',
    method: 'get',
    params
  })
}

// 获取检测历史详情
export function getHistoryDetail(id) {
  return request({
    url: `/history/${id}`,
    method: 'get'
  })
}

// 删除检测历史记录
export function deleteHistory(id) {
  return request({
    url: `/history/${id}`,
    method: 'delete'
  })
}
