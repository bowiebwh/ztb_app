
        
export type Locale = 'zh-CN' | 'en-US';
export type OutputScope = 'all' | 'technical' | 'business';

/**
 * 投标书生成配置模型
 */
export interface GenerationConfigModel {
    /** 唯一 ID */
    id: string;
    /** 输出语言 */
    outputLanguage: Locale;
    /** 输出范围 (全部/技术标/商务标) */
    outputScope: OutputScope;
    /** 输出格式 (目前只支持 Word) */
    outputFormat: 'Word';
}

/**
 * 项目详情页左侧流程导航步骤模型
 */
export interface WorkflowStepModel {
    /** 步骤ID，用于路由跳转 */
    id: string;
    /** 步骤名称 */
    title: string;
    /** Lucide Icon 名称 */
    iconName: string;
    /** 路由路径 */
    routePath: string;
}

export const GENERATION_OUTPUT_SCOPES: Array<{ key: OutputScope, label: string }> = [
    { key: 'all', label: '全部' },
    { key: 'technical', label: '技术标' },
    { key: 'business', label: '商务标' },
];

export const WORKFLOW_STEPS: WorkflowStepModel[] = [
    {
        id: 'upload_tender_document_step',
        title: '上传招标文件',
        iconName: 'Upload',
        routePath: './upload-tender-document-step.html',
    },
    {
        id: 'analyze_tender_content_step',
        title: '招标内容解析',
        iconName: 'Cpu',
        routePath: './analyze-tender-content-step.html',
    },
    {
        id: 'generate_document_step',
        title: '生成文档',
        iconName: 'Sparkles',
        routePath: './generate-document-step.html',
    },
    {
        id: 'edit_bid_document_step',
        title: '投标文档编辑',
        iconName: 'BookOpen',
        routePath: './edit-bid-document-step.html',
    },
    {
        id: 'generate_download_step',
        title: '下载文档',
        iconName: 'Download',
        routePath: './generate-download-step.html',
    },
];

export const DEFAULT_GENERATION_CONFIG: GenerationConfigModel = {
    id: 'config-1',
    outputLanguage: 'zh-CN',
    outputScope: 'all',
    outputFormat: 'Word',
};
        
      
