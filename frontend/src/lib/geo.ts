export type Coordinates = { latitude: number; longitude: number };

const LOCATION_COORDINATES: Record<string, Coordinates> = {
  全国: { latitude: 35.8617, longitude: 104.1954 },
  北京: { latitude: 39.9042, longitude: 116.4074 },
  北京市: { latitude: 39.9042, longitude: 116.4074 },
  上海: { latitude: 31.2304, longitude: 121.4737 },
  上海市: { latitude: 31.2304, longitude: 121.4737 },
  天津: { latitude: 39.3434, longitude: 117.3616 },
  天津市: { latitude: 39.3434, longitude: 117.3616 },
  重庆: { latitude: 29.563, longitude: 106.5516 },
  重庆市: { latitude: 29.563, longitude: 106.5516 },
  石家庄: { latitude: 38.0428, longitude: 114.5149 },
  太原: { latitude: 37.8706, longitude: 112.5489 },
  沈阳: { latitude: 41.8057, longitude: 123.4315 },
  长春: { latitude: 43.8171, longitude: 125.3235 },
  哈尔滨: { latitude: 45.8038, longitude: 126.5349 },
  南京: { latitude: 32.0603, longitude: 118.7969 },
  杭州: { latitude: 30.2741, longitude: 120.1551 },
  湖州: { latitude: 30.8931, longitude: 120.0868 },
  合肥: { latitude: 31.8206, longitude: 117.2272 },
  福州: { latitude: 26.0745, longitude: 119.2965 },
  泉州: { latitude: 24.8741, longitude: 118.6757 },
  南昌: { latitude: 28.682, longitude: 115.8582 },
  济南: { latitude: 36.6512, longitude: 117.1201 },
  枣庄: { latitude: 34.8107, longitude: 117.3237 },
  郑州: { latitude: 34.7466, longitude: 113.6254 },
  新乡: { latitude: 35.303, longitude: 113.9268 },
  洛阳: { latitude: 34.6197, longitude: 112.454 },
  武汉: { latitude: 30.5928, longitude: 114.3055 },
  长沙: { latitude: 28.2282, longitude: 112.9388 },
  广州: { latitude: 23.1291, longitude: 113.2644 },
  韶关: { latitude: 24.8104, longitude: 113.5975 },
  南宁: { latitude: 22.817, longitude: 108.3669 },
  海口: { latitude: 20.044, longitude: 110.1999 },
  成都: { latitude: 30.5728, longitude: 104.0668 },
  贵阳: { latitude: 26.647, longitude: 106.6302 },
  昆明: { latitude: 25.0389, longitude: 102.7183 },
  拉萨: { latitude: 29.652, longitude: 91.1721 },
  西安: { latitude: 34.3416, longitude: 108.9398 },
  兰州: { latitude: 36.0611, longitude: 103.8343 },
  西宁: { latitude: 36.6171, longitude: 101.7782 },
  银川: { latitude: 38.4872, longitude: 106.2309 },
  乌鲁木齐: { latitude: 43.8256, longitude: 87.6168 },
  呼和浩特: { latitude: 40.8426, longitude: 111.7492 },
  河北: { latitude: 38.0428, longitude: 114.5149 },
  山西: { latitude: 37.8706, longitude: 112.5489 },
  辽宁: { latitude: 41.8057, longitude: 123.4315 },
  吉林: { latitude: 43.8171, longitude: 125.3235 },
  黑龙江: { latitude: 45.8038, longitude: 126.5349 },
  江苏: { latitude: 32.0603, longitude: 118.7969 },
  浙江: { latitude: 30.2741, longitude: 120.1551 },
  安徽: { latitude: 31.8206, longitude: 117.2272 },
  福建: { latitude: 26.0745, longitude: 119.2965 },
  江西: { latitude: 28.682, longitude: 115.8582 },
  山东: { latitude: 36.6512, longitude: 117.1201 },
  河南: { latitude: 34.7466, longitude: 113.6254 },
  湖北: { latitude: 30.5928, longitude: 114.3055 },
  湖南: { latitude: 28.2282, longitude: 112.9388 },
  广东: { latitude: 23.1291, longitude: 113.2644 },
  广西: { latitude: 22.817, longitude: 108.3669 },
  海南: { latitude: 20.044, longitude: 110.1999 },
  四川: { latitude: 30.5728, longitude: 104.0668 },
  贵州: { latitude: 26.647, longitude: 106.6302 },
  云南: { latitude: 25.0389, longitude: 102.7183 },
  西藏: { latitude: 29.652, longitude: 91.1721 },
  陕西: { latitude: 34.3416, longitude: 108.9398 },
  甘肃: { latitude: 36.0611, longitude: 103.8343 },
  青海: { latitude: 36.6171, longitude: 101.7782 },
  宁夏: { latitude: 38.4872, longitude: 106.2309 },
  新疆: { latitude: 43.8256, longitude: 87.6168 },
  内蒙古: { latitude: 40.8426, longitude: 111.7492 },
};

function normalize(value?: string | null) {
  if (!value) return undefined;
  return value.replace(/省|市|壮族自治区|回族自治区|维吾尔自治区|自治区/g, '').trim();
}

export function getLocationCoordinates(province?: string | null, city?: string | null): Coordinates | undefined {
  const cityKey = normalize(city);
  if (cityKey && LOCATION_COORDINATES[cityKey]) return LOCATION_COORDINATES[cityKey];
  if (city && LOCATION_COORDINATES[city]) return LOCATION_COORDINATES[city];
  const provinceKey = normalize(province);
  if (provinceKey && LOCATION_COORDINATES[provinceKey]) return LOCATION_COORDINATES[provinceKey];
  if (province && LOCATION_COORDINATES[province]) return LOCATION_COORDINATES[province];
  return undefined;
}
