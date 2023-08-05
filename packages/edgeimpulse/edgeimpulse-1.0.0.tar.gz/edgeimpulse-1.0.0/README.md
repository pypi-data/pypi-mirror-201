# Edge Impulse SDK

This is the official Python SDK for Edge Impulse. It's designed to help ML practitioners build and deploy models that run on embedded hardware.

## Usage

```python
$ pip install edgeimpulse

> import edgeimpulse as ei
> ei.API_KEY = "your-api-key"
> result = ei.model.profile(model="path/to/model")
> result.summary()
```

To learn about the full functionality, see the resources below.

## Resources

* [Overview and getting started](https://docs.edgeimpulse.com/docs/edge-impulse-python-sdk/overview)
* [Tutorial demonstrating how to profile and deploy a model](https://docs.edgeimpulse.com/docs/edge-impulse-python-sdk/01-python-sdk-with-tf-keras)
* [Reference guide](https://docs.edgeimpulse.com/reference/python-sdk/edgeimpulse)
