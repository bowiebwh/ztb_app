-- Create database (adjust name/charset as needed)
CREATE DATABASE IF NOT EXISTS uxbot CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE uxbot;

-- Projects
CREATE TABLE IF NOT EXISTS projects (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) NOT NULL DEFAULT 'Draft',
  current_step_id VARCHAR(100),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Files
CREATE TABLE IF NOT EXISTS files (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NULL,
  filename VARCHAR(255) NOT NULL,
  object_name VARCHAR(255) NOT NULL UNIQUE,
  content_type VARCHAR(128),
  size INT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX(project_id)
);

-- Materials
CREATE TABLE IF NOT EXISTS materials (
  id INT AUTO_INCREMENT PRIMARY KEY,
  type VARCHAR(50) NOT NULL,
  name VARCHAR(255) NOT NULL,
  size INT NOT NULL,
  url VARCHAR(512) NOT NULL,
  thumbnail_url VARCHAR(512),
  icon_name VARCHAR(100),
  upload_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Generation tasks
CREATE TABLE IF NOT EXISTS generation_tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'InProgress',
  progress DOUBLE NOT NULL DEFAULT 0,
  current_stage VARCHAR(100),
  status_message TEXT,
  result_url VARCHAR(512),
  error_message TEXT,
  config_id VARCHAR(100),
  started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX(project_id)
);

-- Tender analysis
CREATE TABLE IF NOT EXISTS tender_analysis (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL,
  summary TEXT,
  key_dates_json TEXT,
  document_structure_json TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX(project_id)
);

CREATE TABLE IF NOT EXISTS document_chunks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL,
  file_id INT NOT NULL,
  chunk_index INT NOT NULL,
  content TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX(project_id),
  INDEX(file_id)
);

CREATE TABLE IF NOT EXISTS pipeline_tasks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL,
  type VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'Pending',
  progress DOUBLE NOT NULL DEFAULT 0,
  result_json TEXT,
  error_message TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX(project_id),
  INDEX(type)
);

CREATE TABLE IF NOT EXISTS document_contents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL UNIQUE,
  content_json LONGTEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS material_bindings (
  id INT AUTO_INCREMENT PRIMARY KEY,
  project_id INT NOT NULL,
  placeholder_key VARCHAR(255) NOT NULL,
  material_id INT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  INDEX(project_id),
  INDEX(placeholder_key)
);

-- Seed data
-- INSERT INTO projects (name, description, status, current_step_id, created_at, updated_at) VALUES
-- ('智慧云招投标系统采购项目 (2025)', '智慧招投标项目，初始状态', 'Draft', 'upload_tender_document_step', '2025-12-15 10:00:00', '2025-12-19 14:30:00'),
-- ('XX银行智慧运营平台建设项目', '生成中示例', 'Generating', 'generate_download_step', '2025-12-18 09:00:00', '2025-12-19 10:00:00'),
-- ('年度服务器与网络设备采购招标', '已完成示例', 'Completed', 'generate_download_step', '2025-12-10 15:00:00', '2025-12-12 16:45:00'),
-- ('教育机构数字化转型服务投标', '失败示例', 'Failed', 'analyze_tender_content_step', '2025-12-05 11:00:00', '2025-12-05 11:30:00'),
-- ('某市数据中心建设项目（招标）', '草稿示例', 'Draft', 'upload_tender_document_step', '2025-11-20 08:00:00', '2025-11-20 08:00:00');

-- INSERT INTO materials (type, name, size, url, thumbnail_url, icon_name, upload_time) VALUES
-- ('Image', '智慧城市架构图.png', 1450000, '/api/files/download_cert_pdf', 'https://spark-builder.s3.cn-north-1.amazonaws.com.cn/image/2025/12/19/3ba8d183-38e6-4008-afe0-747035473be0.png', 'Image', '2025-12-18 10:00:00'),
-- ('Image', '系统部署结构图.jpg', 890000, '/api/files/download_case_study_word', NULL, 'Image', '2025-12-18 11:30:00'),
-- ('PDF', '项目资质证书扫描件.pdf', 2100000, '/api/files/download_cert_pdf', NULL, 'FileText', '2025-12-16 09:00:00'),
-- ('Word', '过往成功案例.docx', 450000, '/api/files/download_case_study_word', NULL, 'ScrollText', '2025-12-15 14:20:00'),
-- ('Excel', '价格配置清单.xlsx', 320000, '/api/files/download_price_excel', NULL, 'LayoutGrid', '2025-12-19 08:00:00');

-- INSERT INTO generation_tasks (project_id, status, progress, current_stage, status_message, result_url, config_id, started_at, updated_at) VALUES
-- (2, 'InProgress', 75, 'Drafting', '章节内容生成中，预计剩余几分钟。', NULL, 'config-1', '2025-12-19 10:00:00', '2025-12-19 10:20:00'),
-- (3, 'Completed', 100, 'Rendering', '投标书 Word 已生成', '/api/files/download_case_study_word', 'config-completed', '2025-12-12 16:00:00', '2025-12-12 16:30:00'),
-- (4, 'Failed', 30, 'Analysis', '招标文件解析失败', NULL, 'config-failed', '2025-12-05 11:00:00', '2025-12-05 11:20:00');

-- INSERT INTO tender_analysis (project_id, summary, key_dates_json, document_structure_json, created_at, updated_at) VALUES
-- (1, '核心需求聚焦高并发、数据安全和扩展性。', '[{"label":"投标截止日期","date":"2026-03-30"},{"label":"项目启动预期","date":"2026-05-01"}]',
--  '[{"id":"ch1","title":"第一章 投标邀请","sections":["投标邀请","招标人信息","招标代理机构"]},{"id":"ch2","title":"第二章 投标人须知","sections":["投标人资格要求","投标文件编制","投标文件递交"]}]',
--  '2025-12-19 10:00:00', '2025-12-19 10:00:00');
