import axios from 'axios';
import qs from 'qs';

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_HOST,
  paramsSerializer: (params) => {
    return qs.stringify(params, { arrayFormat: 'repeat' });
  }
});

export class BaseModel<T> {
  endpoint: string;

  constructor(endpoint: string) {
    this.endpoint = endpoint;
  }

  create(data: any, config: any = {}) {
    return http.post<T>(`${this.endpoint}`, data, config);
  }

  get(id: number | string, params: any = {}) {
    return http.get<T>(`${this.endpoint}${id}/`, { params });
  }

  list(params: any = {}) {
    return http.get<T[]>(`${this.endpoint}`, { params });
  }

  update(id: number | string, data: any, config = {}, patch = true) {
    if (patch) {
      return http.patch<T>(`${this.endpoint}${id}/`, data, config);
    }
    return http.put<T>(`${this.endpoint}${id}/`, data, config);
  }

  delete(id: number | string) {
    return http.delete(`${this.endpoint}${id}/`);
  }

  detailAction(
    id: number | string,
    action: string,
    method: string,
    data: any = {},
    params: any = {},
    config: any = {}
  ) {
    return http.request({
      url: `${this.endpoint}${id}/${action}/`,
      method,
      data,
      params,
      ...config,
    });
  }

  listAction(action: string, method: string, data: any = {}, params: any = {}, config: any = {}) {
    return http.request({
      url: `${this.endpoint}${action}/`,
      method,
      data,
      params,
      ...config,
    });
  }
}
