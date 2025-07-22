export interface ReportListAPIResponse {
    count: number;
    next: null;
    previous: null;
    results: Report[];
}

export interface Report {
    id: number;
    title: string;
    description: string;
    category: {
        id: number;
        name: string;
        slug: string;
        name_nepali?: string;
        color: string;
    };
    status: string;
    image: string;
    location_lat: number;
    location_lng: number;
    address: string;
    created_by: {
        id: number;
        full_name: string;
    };
    created_at: string;
    updated_at: string;
    is_flagged: boolean;
    up_votes: number;
    has_upvoted: boolean;
    has_reported: boolean;
    emotions: [
        {
            text: { id: number; content: string };
            emotion: string;
            score: number;
            all_emotions: {
                neutral: number;
                sadness: number;
                fear: number;
                surprise: number;
                joy: number;
                anger: number;
                disgust: number;
            };
        }
    ];
}

export interface Category {
    id: number;
    name: string;
    slug: string;
    name_nepali: string;
    color: string;
    report_count: number;
}
