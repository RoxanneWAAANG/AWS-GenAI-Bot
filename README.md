# Project 4 -- AWS Generative AI Text Generation Service

A production-ready, enterprise-grade AI text generation service built on AWS serverless architecture with comprehensive security, monitoring, and content filtering capabilities.

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │    │   Lambda Layer   │    │  AI & Storage   │
│                 │    │                  │    │                 │
│ • REST Endpoints│───▶│ • Text Generator │───▶│ • AWS Bedrock   │
│ • CORS Config   │    │ • Usage Stats    │    │ • Claude 4      │
│ • Rate Limiting │    │ • Content Filter │    │ • DynamoDB      │
│ • OpenAPI Docs  │    │ • Input Validation│    │ • CloudWatch    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
          │                       │                       │
          │            ┌──────────────────┐              │
          │            │  Security Layer  │              │
          └───────────▶│                  │◀─────────────┘
                       │ • IAM Policies   │
                       │ • Content Filter │
                       │ • Audit Logging  │
                       │ • Input Sanitization
                       └──────────────────┘
```

### Core Components

- **API Gateway**: RESTful API endpoints with built-in throttling and CORS
- **Lambda Functions**: Serverless compute for text generation and analytics
- **AWS Bedrock**: Managed AI service with Claude 4 Sonnet model
- **DynamoDB**: NoSQL database for usage tracking and analytics
- **CloudWatch**: Comprehensive monitoring, logging, and alerting
- **IAM**: Fine-grained access control and security policies

## Features

### Core Functionality
- **Text Generation**: High-quality AI-powered text generation with Claude 4 Sonnet
- **Configurable Parameters**: Adjustable max tokens, temperature, and user tracking
- **RESTful API**: Standard HTTP endpoints with JSON request/response
- **Auto-scaling**: Serverless architecture that scales automatically

### Security & Content Filtering
- **Multi-layer Content Filtering**: Pattern-based and AI-powered content detection
- **Input Validation**: Comprehensive request sanitization and validation
- **Output Filtering**: AI response screening for policy compliance
- **Security Logging**: Detailed audit trails for all security events
- **IAM Integration**: Role-based access control with least privilege principles

### Monitoring & Analytics
- **Usage Tracking**: Per-user request and token consumption metrics
- **Performance Monitoring**: Response time and throughput analytics
- **Real-time Dashboards**: CloudWatch integration for operational visibility
- **Cost Optimization**: Token usage tracking for budget management
- **Alerting**: Automated notifications for anomalies and issues

### Developer Experience
- **OpenAPI Documentation**: Complete API specification with examples
- **Error Handling**: Comprehensive error responses with actionable messages
- **Rate Limiting**: Built-in protection against abuse and overuse
- **CORS Support**: Web application integration ready

## Technical Stack

- **Compute**: AWS Lambda (Python 3.9)
- **API**: Amazon API Gateway (REST API)
- **AI**: AWS Bedrock (Claude 4 Sonnet)
- **Database**: Amazon DynamoDB
- **Monitoring**: Amazon CloudWatch
- **Security**: AWS IAM, AWS Comprehend
- **Infrastructure**: AWS SAM (Serverless Application Model)

## Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/RoxanneWAAANG/AWS-GenAI-Bot.git
cd AWS-GenAI-Bot
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure AWS Bedrock Access
1. Navigate to AWS Bedrock Console
2. Go to "Model access" in the sidebar
3. Request access to "Claude 4 Sonnet" model
4. Wait for approval (usually 5-30 minutes)

### 3. Deploy the Service
```bash
sam build
sam deploy --guided
```

Follow the prompts:
- Stack Name: `genai-bot`
- AWS Region: `us-east-2`
- Confirm changes: `Y`
- Allow IAM role creation: `Y`
- Disable rollback: `Y`
- Save parameters: `Y`

### 4. Test the Deployment
```bash
export API_URL="https://2i9yquihz5.execute-api.us-east-2.amazonaws.com/Prod"

# Test text generation
curl -X POST "$API_URL/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a short poem about AI", "user_id": "test_user"}'

# Test usage statistics
curl "$API_URL/usage/test_user"
```

## API Reference

### Text Generation Endpoint

**POST** `/generate`

Generate AI-powered text based on user prompts.

#### Request Body
```json
{
  "prompt": "Your text prompt here",
  "max_tokens": 1000,
  "temperature": 0.7,
  "user_id": "unique_user_identifier"
}
```

#### Parameters
- `prompt` (required): The input text prompt for generation
- `max_tokens` (optional): Maximum tokens in response (default: 1000)
- `temperature` (optional): Creativity level 0.0-1.0 (default: 0.7)
- `user_id` (optional): User identifier for tracking (default: "anonymous")

#### Response
```json
{
  "generated_text": "AI-generated response text...",
  "metadata": {
    "input_tokens": 5,
    "output_tokens": 42,
    "response_time_ms": 185,
    "model_id": "anthropic.claude-sonnet-4-20250514-v1:0",
    "user_id": "test_user",
    "content_filter_status": "passed"
  }
}
```

#### Error Responses

**400 Bad Request - Content Policy Violation**
```json
{
  "error": "Content policy violation detected",
  "details": {
    "reason": "Content policy violation",
    "severity": "MEDIUM",
    "user_id": "user123",
    "timestamp": 1719068745
  },
  "message": "Your request contains content that violates our usage policies."
}
```

**400 Bad Request - Missing Prompt**
```json
{
  "error": "Prompt is required"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error: [error details]"
}
```

### Usage Statistics Endpoint

**GET** `/usage/{user_id}`

Retrieve usage analytics for a specific user.

#### Parameters
- `user_id` (path): User identifier
- `days` (query, optional): Number of days to include (default: 7)

#### Example Request
```bash
curl "https://2i9yquihz5.execute-api.us-east-2.amazonaws.com/Prod/usage/user123?days=30"
```

#### Response
```json
{
  "user_id": "user123",
  "period_days": 30,
  "total_requests": 47,
  "total_input_tokens": 1250,
  "total_output_tokens": 3890,
  "average_response_time_ms": 185,
  "requests_by_day": [
    {
      "date": "2025-06-22",
      "requests": 8,
      "tokens": 421
    }
  ],
  "content_filter_events": 2,
  "last_request": "2025-06-22T16:45:32Z",
  "status": "active"
}
```

## Security Features

### Content Filtering

The service implements multi-layer content filtering:

1. **Input Filtering**: Scans prompts for harmful patterns
2. **Pattern Matching**: Detects policy violations using keyword analysis
3. **AI-Based Filtering**: Uses AWS Comprehend for sentiment analysis
4. **Output Filtering**: Screens AI responses for policy compliance

### Blocked Content Categories
- Harmful and violent content
- Inappropriate or explicit material
- Discriminatory language
- Illegal activities
- Toxic or offensive content

### Security Logging

All security events are logged with:
- User identification
- Timestamp and request details
- Content filter results
- Severity classification
- Audit trail for compliance

## Monitoring

### CloudWatch Metrics

The service automatically publishes metrics to CloudWatch:

- **Request Volume**: Total API requests per time period
- **Response Times**: Average and percentile response times
- **Token Usage**: Input and output token consumption
- **Error Rates**: 4xx and 5xx error percentages
- **Content Filter Events**: Security event frequency

### Usage Analytics

Per-user analytics include:
- Request patterns and frequency
- Token consumption trends
- Response time performance
- Content filter event history

### Alerting

Recommended CloudWatch alarms:
- High error rates (>5% 5xx errors)
- Unusual request spikes (>1000% increase)
- Content filter anomalies (>10 events/hour)
- High response times (>2000ms average)

## Configuration

### Environment Variables

Configure the service through template.yaml:

```yaml
Environment:
  Variables:
    USAGE_TABLE_NAME: !Ref UsageTable
    CONTENT_FILTER_ENABLED: "true"
    LOG_LEVEL: "INFO"
```

### IAM Policies

The service uses least-privilege IAM policies:
- Bedrock model invocation permissions
- DynamoDB read/write access
- CloudWatch logging permissions
- Comprehend API access for content filtering

## Testing

### Unit Tests
```bash
# Run tests (when implemented)
python -m pytest tests/
```

### Manual Testing
```bash
# Test content filtering
curl -X POST "$API_URL/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Generate harmful content", "user_id": "test"}'

# Test normal operation
curl -X POST "$API_URL/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a haiku about technology", "user_id": "test"}'
```

## Deployment

### Production Considerations

1. **Enable Real Bedrock Mode**:
   ```python
   # In chatbot/app.py
   USE_BEDROCK = True
   ```

2. **Configure Production Monitoring**:
   - Set up CloudWatch dashboards
   - Configure alerting rules
   - Enable detailed logging

3. **Security Hardening**:
   - Review IAM policies
   - Enable VPC endpoints if needed
   - Configure API Gateway request validation

4. **Performance Optimization**:
   - Tune Lambda memory allocation
   - Configure reserved concurrency
   - Implement response caching if appropriate

### Multi-Region Deployment

For high availability:
1. Deploy to multiple AWS regions
2. Use Route 53 for DNS failover
3. Configure cross-region DynamoDB replication
4. Set up CloudWatch cross-region monitoring
