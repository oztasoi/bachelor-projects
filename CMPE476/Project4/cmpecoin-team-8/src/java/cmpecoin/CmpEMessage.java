package cmpecoin;

import com.google.gson.Gson;

public class CmpEMessage {

    public static class Builder {

        private CmpEMessageType messageType;
        private String sourceAddress;
        private String targetAddress;
        private String jsonString;
        private Long timestamp;

        public CmpEMessage create(){
            CmpEMessage message = new CmpEMessage();
            message.messageType = this.messageType;
            message.sourceAddress = this.sourceAddress;
            message.targetAddress = this.targetAddress;
            message.jsonString = this.jsonString;
            message.timestamp = this.timestamp;

            return message;
        }

        public Builder withType(CmpEMessageType _messageType){
            this.messageType = _messageType;
            return this;
        }

        public Builder fromSource(String _source){
            this.sourceAddress = _source;
            return this;
        }

        public Builder toTarget(String _target){
            this.targetAddress = _target;
            return this;
        }

        public Builder addJson(String _jsonString){
            this.jsonString = _jsonString;
            return this;
        }

        public Builder atUNIX(Long _timestamp){
            this.timestamp = _timestamp;
            return this;
        }
    }

    private CmpEMessageType messageType;
    private String sourceAddress;
    private String targetAddress;
    private String jsonString;
    private Long timestamp;

    private CmpEMessage(){

    }

    public CmpEMessageType getMessageType() {
        return messageType;
    }

    public void setMessageType(CmpEMessageType messageType) {
        this.messageType = messageType;
    }

    public String getSourceAddress() {
        return sourceAddress;
    }

    public void setSourceAddress(String sourceAddress) {
        this.sourceAddress = sourceAddress;
    }

    public String getTargetAddress() {
        return targetAddress;
    }

    public void setTargetAddress(String targetAddress) {
        this.targetAddress = targetAddress;
    }

    public String getJsonString() {
        return jsonString;
    }

    public Object getJsonDeserialized(Object obj) {
        Gson gson = new Gson();
        return gson.fromJson(jsonString, obj.getClass());
    }

    public void setJsonString(String jsonString) {
        this.jsonString = jsonString;
    }

    public Long getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Long timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String toString(){
        Gson gson = new Gson();
        return gson.toJson(this);
    }

    public static String jsonify(Object _object){
        Gson gson = new Gson();
        return gson.toJson(_object);
    }

    public static CmpEMessage fromString(String _message){
        Gson gson = new Gson();
        return (CmpEMessage) gson.fromJson(_message, CmpEMessage.class);
    }
}
