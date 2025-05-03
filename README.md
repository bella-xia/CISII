## To run in Experimental Setting

1. open rospy system using roslaunch
2. run `python3 image_based_puncture_detection_modulerized.py`
3. after an interface window has appeared, use another window to run `python record_from_rostopics_new.py`

## Visualize interface post-experiment

1. run `python3 _utils_postprocess/post_trial_visualization --path <folder path for al the data>`

## Debug Suggestions

1. If there is a problem in the actual procedure of the main workflow, check

- **image_based_puncture_detection_modulerized.py** --> giving the flow for subscribing to
  each microscope images and running CNN models
- **record_from_rostopics_new.py** --> subscribing to all publishing data and
  aggregate them into a csv file

2. if the error is in the microscope image processing flow, check for scripts in \_utils_model

- **image_based_util_unet.py** --> use the pretrained UNET model to process input image data
- **image_based_util_dbscan.py** --> helper function to util_unet: cluster segmentation
  result and only output the largest and reasonably sized segmentation area
- **image_based_util_kalman.py** --> helper function to util_unet: conduct Kalman Filter
  on the needle tip displacement data
- **image_based_util_visualization.py** --> visualization interface that provides velocity,
  segmentation information, and puncture detection in real-time

  3. if an error occurs in the rospy publication / subscription part, refer to \_utils_rospy

- **publisher_module.py** --> modularized deployment of rospy publisher.
  If working properly, user can use

  ```
  PubRosTopic(
    <publication topic>,
    <data type>,
    <publisher attribute>,
    )
  ```

To declare a published ros topic, and use

```
manager = RosTopicPublisher([... list of PubPosTopic ...])
```

To create a ros publisher manager. To later publish data,
user can use

```
manager.publish_data(
    [... a list of publisher attribute name ... ],
    [... a list of corresponding data ... ]
    )
```

To systematically publish data

- **subscriber_module.py** --> modularized deployment of rospy subscriber.
  If working properly, user can use

```
SubRosTopic(
    <subscription topic>,
    <data type>,
    <subscriber attribute>,
    <subscribe data attribute>,
)
```

To declare a subscribed ros topic,
and use

```
manager = RosTopicSubscriber([... list of SubPosTopic ...])
```

To create a ros subscriber manager. After setting it up, each
subscribed topic can be accessed via `manager.<subscribe data attribute>` and each subscriber itself via `manager.<subscriber attribute>`.
