# API Documentation

## Translate API

```typescript
{

"from" : string // source language 
"to" : string, // target language
"from_text" : string, // text to be translated
"id" : int // request id
}
```

Response
```typescript
{
"to_text" : string, // translated text
"id" : int // request id
}
```

## Installing Python Dependencies

```bash
pip install -r requirements.txt
```

## Testing 

To launch a testing server:

```bash
python3 -m flask run
```

... from [`src/`](./src).

