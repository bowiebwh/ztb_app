
export interface Chapter {
  id: string
  title: string
  level: number
  children?: Chapter[]
}

export interface ContentBlock {
  type: 'heading' | 'paragraph' | 'image' | 'table' | 'list' | 'quote'
  level?: number
  content?: string
  items?: string[]
  src?: string
  alt?: string
  rows?: Array<string[]>
  headers?: string[]
}

export interface BidDocument {
  id: string
  projectName: string
  chapters: Chapter[]
  content: Record<string, ContentBlock[]>
}

export const mockBidDocument: BidDocument = {
  id: 'bid-doc-001',
  projectName: '企业级招投标文档智能生成系统',
  chapters: [
    {
      id: 'chapter-1',
      title: '第一章 投标人资格声明',
      level: 1,
      children: [
        {
          id: 'chapter-1-1',
          title: '1.1 基本信息',
          level: 2,
        },
        {
          id: 'chapter-1-2',
          title: '1.2 资质证明',
          level: 2,
        },
      ],
    },
    {
      id: 'chapter-2',
      title: '第二章 技术方案',
      level: 1,
      children: [
        {
          id: 'chapter-2-1',
          title: '2.1 系统架构',
          level: 2,
        },
        {
          id: 'chapter-2-2',
          title: '2.2 技术实现',
          level: 2,
        },
        {
          id: 'chapter-2-3',
          title: '2.3 安全保障',
          level: 2,
        },
      ],
    },
    {
      id: 'chapter-3',
      title: '第三章 商务方案',
      level: 1,
      children: [
        {
          id: 'chapter-3-1',
          title: '3.1 价格清单',
          level: 2,
        },
        {
          id: 'chapter-3-2',
          title: '3.2 付款条款',
          level: 2,
        },
      ],
    },
    {
      id: 'chapter-4',
      title: '第四章 项目管理',
      level: 1,
      children: [
        {
          id: 'chapter-4-1',
          title: '4.1 项目计划',
          level: 2,
        },
        {
          id: 'chapter-4-2',
          title: '4.2 质量保证',
          level: 2,
        },
      ],
    },
  ],
  content: {
    'chapter-1': [
      {
        type: 'heading',
        level: 2,
        content: '1.1 基本信息',
      },
      {
        type: 'paragraph',
        content: '本投标人是一家具有多年行业经验的专业企业，拥有完整的资质证明和技术能力。我们致力于为客户提供高质量的解决方案和优质的服务。',
      },
      {
        type: 'table',
        headers: ['项目', '内容'],
        rows: [
          ['企业名称', '智标科技有限公司'],
          ['统一社会信用代码', '91110000MA00000000'],
          ['注册资本', '1000万元'],
          ['成立时间', '2020年1月'],
        ],
      },
      {
        type: 'heading',
        level: 2,
        content: '1.2 资质证明',
      },
      {
        type: 'list',
        items: [
          '高新技术企业认证证书',
          'ISO 9001质量管理体系认证',
          'ISO 27001信息安全管理体系认证',
          '软件著作权证书（5项）',
        ],
      },
    ],
    'chapter-1-1': [
      {
        type: 'heading',
        level: 2,
        content: '1.1 基本信息',
      },
      {
        type: 'paragraph',
        content: '本投标人是一家具有多年行业经验的专业企业，拥有完整的资质证明和技术能力。',
      },
      {
        type: 'table',
        headers: ['项目', '内容'],
        rows: [
          ['企业名称', '智标科技有限公司'],
          ['统一社会信用代码', '91110000MA00000000'],
          ['注册资本', '1000万元'],
        ],
      },
    ],
    'chapter-1-2': [
      {
        type: 'heading',
        level: 2,
        content: '1.2 资质证明',
      },
      {
        type: 'paragraph',
        content: '我们拥有以下主要资质和认证：',
      },
      {
        type: 'list',
        items: [
          '高新技术企业认证证书',
          'ISO 9001质量管理体系认证',
          'ISO 27001信息安全管理体系认证',
          '软件著作权证书（5项）',
        ],
      },
    ],
    'chapter-2': [
      {
        type: 'heading',
        level: 2,
        content: '2.1 系统架构',
      },
      {
        type: 'paragraph',
        content: '本系统采用现代化的微服务架构设计，确保系统的高可用性、高性能和易扩展性。',
      },
      {
        type: 'image',
        src: 'https://spark-builder.s3.cn-north-1.amazonaws.com.cn/image/2025/12/19/1b00ef03-1628-40b2-9d83-8b16e4a1b927.png',
        alt: '系统架构图',
      },
      {
        type: 'heading',
        level: 2,
        content: '2.2 技术实现',
      },
      {
        type: 'paragraph',
        content: '系统采用以下核心技术栈：',
      },
      {
        type: 'list',
        items: [
          'Vue 3 + TypeScript 前端框架',
          'Node.js + Express 后端服务',
          'PostgreSQL 数据库',
          'Redis 缓存层',
          'Docker 容器化部署',
        ],
      },
      {
        type: 'heading',
        level: 2,
        content: '2.3 安全保障',
      },
      {
        type: 'paragraph',
        content: '我们采用多层安全防护措施，确保系统和数据的安全性：',
      },
      {
        type: 'list',
        items: [
          'HTTPS/TLS 加密传输',
          'JWT 身份认证',
          '角色基访问控制（RBAC）',
          '数据加密存储',
          '定期安全审计',
        ],
      },
    ],
    'chapter-2-1': [
      {
        type: 'heading',
        level: 2,
        content: '2.1 系统架构',
      },
      {
        type: 'paragraph',
        content: '本系统采用现代化的微服务架构设计，确保系统的高可用性、高性能和易扩展性。',
      },
      {
        type: 'image',
        src: 'https://spark-builder.s3.cn-north-1.amazonaws.com.cn/image/2025/12/19/d8097976-ee42-48a5-a8d8-acf0bd2601cd.png',
        alt: '系统架构图',
      },
    ],
    'chapter-2-2': [
      {
        type: 'heading',
        level: 2,
        content: '2.2 技术实现',
      },
      {
        type: 'paragraph',
        content: '系统采用以下核心技术栈：',
      },
      {
        type: 'list',
        items: [
          'Vue 3 + TypeScript 前端框架',
          'Node.js + Express 后端服务',
          'PostgreSQL 数据库',
          'Redis 缓存层',
          'Docker 容器化部署',
        ],
      },
    ],
    'chapter-2-3': [
      {
        type: 'heading',
        level: 2,
        content: '2.3 安全保障',
      },
      {
        type: 'paragraph',
        content: '我们采用多层安全防护措施，确保系统和数据的安全性：',
      },
      {
        type: 'list',
        items: [
          'HTTPS/TLS 加密传输',
          'JWT 身份认证',
          '角色基访问控制（RBAC）',
          '数据加密存储',
          '定期安全审计',
        ],
      },
    ],
    'chapter-3': [
      {
        type: 'heading',
        level: 2,
        content: '3.1 价格清单',
      },
      {
        type: 'paragraph',
        content: '以下为本项目的详细价格清单：',
      },
      {
        type: 'table',
        headers: ['项目', '单价（万元）', '数量', '合计（万元）'],
        rows: [
          ['系统开发', '50', '1', '50'],
          ['部署实施', '10', '1', '10'],
          ['培训服务', '5', '1', '5'],
          ['一年维保', '8', '1', '8'],
        ],
      },
      {
        type: 'paragraph',
        content: '合计：73万元',
      },
      {
        type: 'heading',
        level: 2,
        content: '3.2 付款条款',
      },
      {
        type: 'list',
        items: [
          '合同签订后支付30%（21.9万元）',
          '系统上线后支付50%（36.5万元）',
          '验收合格后支付20%（14.6万元）',
        ],
      },
    ],
    'chapter-3-1': [
      {
        type: 'heading',
        level: 2,
        content: '3.1 价格清单',
      },
      {
        type: 'paragraph',
        content: '以下为本项目的详细价格清单：',
      },
      {
        type: 'table',
        headers: ['项目', '单价（万元）', '数量', '合计（万元）'],
        rows: [
          ['系统开发', '50', '1', '50'],
          ['部署实施', '10', '1', '10'],
          ['培训服务', '5', '1', '5'],
          ['一年维保', '8', '1', '8'],
        ],
      },
    ],
    'chapter-3-2': [
      {
        type: 'heading',
        level: 2,
        content: '3.2 付款条款',
      },
      {
        type: 'paragraph',
        content: '付款分三个阶段进行：',
      },
      {
        type: 'list',
        items: [
          '合同签订后支付30%（21.9万元）',
          '系统上线后支付50%（36.5万元）',
          '验收合格后支付20%（14.6万元）',
        ],
      },
    ],
    'chapter-4': [
      {
        type: 'heading',
        level: 2,
        content: '4.1 项目计划',
      },
      {
        type: 'paragraph',
        content: '项目总周期为6个月，具体计划如下：',
      },
      {
        type: 'table',
        headers: ['阶段', '工作内容', '周期'],
        rows: [
          ['需求分析', '需求调研、方案设计', '1个月'],
          ['系统开发', '核心功能开发、单元测试', '3个月'],
          ['测试部署', '系统测试、部署实施', '1个月'],
          ['验收交付', '用户验收、培训交付', '1个月'],
        ],
      },
      {
        type: 'heading',
        level: 2,
        content: '4.2 质量保证',
      },
      {
        type: 'paragraph',
        content: '我们承诺提供以下质量保证：',
      },
      {
        type: 'list',
        items: [
          '代码审查和单元测试覆盖率≥80%',
          '系统可用性≥99.9%',
          '响应时间<2秒',
          '一年免费维保期',
          '24小时技术支持',
        ],
      },
    ],
    'chapter-4-1': [
      {
        type: 'heading',
        level: 2,
        content: '4.1 项目计划',
      },
      {
        type: 'paragraph',
        content: '项目总周期为6个月，具体计划如下：',
      },
      {
        type: 'table',
        headers: ['阶段', '工作内容', '周期'],
        rows: [
          ['需求分析', '需求调研、方案设计', '1个月'],
          ['系统开发', '核心功能开发、单元测试', '3个月'],
          ['测试部署', '系统测试、部署实施', '1个月'],
          ['验收交付', '用户验收、培训交付', '1个月'],
        ],
      },
    ],
    'chapter-4-2': [
      {
        type: 'heading',
        level: 2,
        content: '4.2 质量保证',
      },
      {
        type: 'paragraph',
        content: '我们承诺提供以下质量保证：',
      },
      {
        type: 'list',
        items: [
          '代码审查和单元测试覆盖率≥80%',
          '系统可用性≥99.9%',
          '响应时间<2秒',
          '一年免费维保期',
          '24小时技术支持',
        ],
      },
    ],
  },
}
